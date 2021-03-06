#!/usr/bin/python
# -*- coding: latin-1 -*-

import os
import sys
import arcpy
import datetime
#reload(sys)
#sys.setdefaultencoding("utf8")

from reportlab.lib.pagesizes import letter, cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER,TA_JUSTIFY,TA_LEFT,TA_RIGHT
from reportlab.lib.units import inch
from reportlab.lib import colors

styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
styles.add(ParagraphStyle(name='Left', alignment=TA_LEFT))
styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))
styles.add(ParagraphStyle(name='Right', alignment=TA_RIGHT))
styles.add(ParagraphStyle(name='Tabla', alignment=TA_JUSTIFY, fontSize=6.5))

#importar utf8
#Parametros
#arcpy.env.overwriteOutput=True
#tablaEntrada=r"X:\PRUEBAS\ReportePagos_2015\Datos_Prueba.gdb\DATOS_PRUEBA"
#tablaEstadisticas="in_memory\TablaEstadisticas"
#ActividadContractual="Edicion"
#pdfSalida =r"X:\PRUEBAS\PDF\simple_table_grid13.pdf"
#NoContrato="12245-2013"
#periodo = "2015-01-01 al 2015-02-01"
#Parametros

tablaEntrada=sys.argv[1]
ActividadContractual=sys.argv[2]
NoContrato=sys.argv[3]
reportarPeriodo=sys.argv[4]
periodo = sys.argv[5]
pdfSalida =sys.argv[6]

tablaEstadisticas="in_memory\TablaEstadisticas"

def calcularDescripcion(tabla,dominio,campo):
    try:
        desc=arcpy.Describe(tablaEntrada)
        arcpy.DomainToTable_management(os.path.dirname(desc.catalogPath),dominio,"in_memory/dominioOut","codigo","descripcion")
        rows= arcpy.SearchCursor("in_memory/dominioOut")
        dom={}
        for row in rows:
            dom[row.getValue ("codigo")]=row.getValue ("descripcion")
        rowsup = arcpy.UpdateCursor(tabla,"","",campo)
        for rowup in rowsup:
            for key, value in dom.items():
                if key==rowup.getValue (campo):
                    rowup.setValue (campo, value)
                rowsup.updateRow(rowup)
        arcpy.Delete_management("in_memory/dominioOut")
    except Exception as e:
        arcpy.AddMessage("Error Calculando Descripcion: "+ e.message)

def TablaArray(table,fields):
    array=[]
    try:
        rows = arcpy.SearchCursor(table)
        encabezado=[]

        for field in fields:
            if field == "ACTIVIDAD":
                encabezado.append(Paragraph("<B>Actividades Relacionadas seg�n Contrato</B>",styles["Center"]))
            elif field == "SUM_ADMIN_GIT_PC_PAGOS_AREA":
                encabezado.append(Paragraph("<B>Area HA</B>",styles["Center"]))
            elif field == "SUM_VALOR_PAGADO":
                encabezado.append(Paragraph("<B>Valor</B>",styles["Center"]))
            else:
                encabezado.append(Paragraph("<B>"+field.title()+"</B>",styles["Center"]))
        array.append(encabezado)
        print encabezado
        for row in rows:
            arrayrow=[]
            for field in fields:
                if row.getValue(field)==None:
                    arrayrow.append(Paragraph("",styles["Tabla"]))
                else:
                    arrayrow.append(Paragraph(str(row.getValue(field)),styles["Tabla"]))
            array.append(arrayrow)
        return array
    except Exception as e:
        arcpy.AddMessage(e.message)
        return array
def suma(table,campo):
    rows = arcpy.SearchCursor(table)
    try:
        sumatoria=0.0
        for row in rows:
            sum=row.getValue(campo)
            sumatoria+=sum
        return sumatoria
    except Exception as e:
        arcpy.AddMessage("Error sumando Campo: " + e.message)
        return 0.0


def valorUnico(table,campo):
    rows = arcpy.SearchCursor(table)
    PrimerValor=""
    try:
        for row in rows:
            PrimerValor=row.getValue(campo)
            break
        else:
            pass
        return PrimerValor
    except Exception as e:
        arcpy.AddMessage("Error En el Campo Responsable: "+ e.message)
        return ""


result = int(arcpy.GetCount_management(tablaEntrada).getOutput(0))
if result<2000:
    try:
        camposSum= [["ADMIN_GIT_PC.PAGOS.AREA","SUM"],["VALOR_PAGADO","SUM"]]
        camposUnicos= ["ESCALA","ACTIVIDAD","PROYECTO"]
        fields=["ACTIVIDAD","PROYECTO","ESCALA","SUM_ADMIN_GIT_PC_PAGOS_AREA","SUM_VALOR_PAGADO"]
        arcpy.Statistics_analysis(tablaEntrada, tablaEstadisticas, camposSum, camposUnicos)
        calcularDescripcion(tablaEstadisticas,"DOM_PAGOS_ESCALA","ESCALA")
        calcularDescripcion(tablaEstadisticas,"Dom_Actividad_Pagos","ACTIVIDAD")
        calcularDescripcion(tablaEstadisticas,"Dom_Proyecto_Pagos2","PROYECTO")
        data=TablaArray(tablaEstadisticas,fields)

        ##Formateo de Actividad y Proyecto

        ####################
        width, height = letter
        doc = SimpleDocTemplate(pdfSalida, pagesize=letter)
        elements = []
        #Alineacion

        # FECHA

        fecha= datetime.date.today()
        hoy= "Bogot� "+fecha.strftime("%d/%m/%Y")

        fechapara=Paragraph(hoy, styles["Left"])
        elements.append(fechapara)

        elements.append(Spacer(0, inch*.3))

        # creamos t�tulo con estilo
        titulo = Paragraph("INFORME DE PRODUCCI�N",styles["Center"])
        elements.append(titulo)
        # Contrato
        contratotxt = Paragraph("CONTRATO No. <strong>%s</strong>"%(NoContrato),styles["Center"])
        elements.append(contratotxt)
        #Periodo
        if reportarPeriodo=="true":
            periodotxt=Paragraph("Peri�do a Reportar <strong>%s</strong>"%(periodo),styles["Center"])
            elements.append(periodotxt)
        elements.append(Spacer(0, inch*.3))

        actividadesTitulo =Paragraph("<strong>ACTIVIDADES DEL CONTRATO</strong>",styles["Right"])
        # espacio adicional
        elements.append(Spacer(0, inch*.1))

        def actividades(Actividad):
            texActividades=[]
            if Actividad=="Control Restitucion":
                texActividades.append("Obligaciones del contratista:")
                texActividades.append("2.1- Validar en estaci�n digital la correcta captura de los elementos altim�tricos y planim�tricos o modelos digitales del terreno,obtenidos mediante restituci�n \
                                       por funcionarios y contratistas del �rea, a diferentes escalas, de acuerdo con las asignaciones y plan del trabajo del �rea t�cnica.")
                texActividades.append("2.2- Verificar la consistencia tem�tica, consistencia l�gica, la totalidad de la informaci�n. La correcta posici�n y los empalmes y conectividad entre niveles.")
                texActividades.append("2.3- Diligenciar los formatos respectivos del control de calidad realizado a cada proyecto.")

            elif Actividad=="Control Calidad Digital":
                texActividades.append("Obligaciones del contratista:")
                texActividades.append("2.1 Realizar el diagn�stico general y evaluar la calidad de la informaci�n cartogr�fica digital producida por actualizaci�n de las hojas cartogr�ficas a las diferentes escalas de producci�n.")
                texActividades.append("2.2 Realizar el control de estandarizaci�n de la informaci�n para lo cual la contratista debe revisar el grado de totalidad, consistencia l�gica, consistencia tem�tica, exactitud en posici�n,\
                                        de la informaci�n digital de acuerdo con el catalogo de objetos y el modelo de datos IGAC y comprobar que sean efectuadas las correcciones solicitadas a los procesos de edici�n y estructuraci�n,\
                                        elaborar los metadatos correspondientes a cada una de las planchas efectuadas.")
                texActividades.append("2.3 Realizar los complementos y ajustes necesarios que resulten del control digital y de los procesos de revisi�n y control de calidad y los lineamientos del coordinador del proyecto.")
                texActividades.append("2.4 Diligenciar y documentar las actividades de acuerdo con los formatos establecidos por la subdirecci�n de geograf�a y cartograf�a.")
                texActividades.append("2.12 Verificar los empalmes para cada una de las hojas en cada uno de los lados que esta  presente y para cada uno de los elementos cartograficos.")
            elif Actividad=="Actualizacion 100K":
                texActividades.append("Obligaciones del contratista:")
                texActividades.append("2.1 Cumplir con el plan de trabajo establecido para el objecto a desarrollar.")
                texActividades.append("2.2 Realizar la captura de los elementos planim�tricos conforme a las tolerancias para la escala, a partir de im�genes \
                                        �pticas y de radar necesarias para el mantenimiento de las bases de datos cartograficas de la subdirecci�n de geografia y cartografia.")
                texActividades.append("2.4 Actualizar las salidas gr�ficas convencionales de acuerdo con el formato aprobado para tal fin.")
                texActividades.append("2.5 Realizar las salidas gr�ficas de mapa plegado de acuerdo con el formato aprobado para tal fin.")
                texActividades.append("2.6 Edici�n de toponimia conforme a los requerimientos definido para la base de datos multiescala.")
            elif Actividad=="Control Actualizacion":
                texActividades.append("Obligaciones del contratista:")
                texActividades.append("2.1 Realizar el diagn�stico general y evaluar la calidad de la informaci�n cartogr�fica digital producida por actualizaci�n de las hojas cartogr�ficas a las diferentes escalas de producci�n.")
                texActividades.append("2.2 Realizar el control de estandarizaci�n de la informaci�n para lo cual el contratista debe revisar el grado de totalidad, consistencia l�gica, consistencia tem�tica, exactitud en posici�n, \
                                        de la informaci�n digital de acuerdo con el cat�logo de objetos y el modelo de datos IGAC y comprobar que sean efectuadas las correcciones solicitadas a los procesos de edici�n, \
                                        digitalizaci�n y estructuraci�n, elaborar los metadatos correspondientes a cada una de las planchas efectuadas.")
                texActividades.append("2.3 Realizar los complementos y ajustes necesarios que resulten del control digital y de los procesos de revisi�n y control de calidad y los lineamientos del coordinador del proyecto.")
                texActividades.append("2.5 Diligenciar y documentar las actividades de acuerdo con los formatos establecidos por la subdirecci�n de geograf�a y cartograf�a.")
            elif Actividad=="Control Calidad Grafico":
                texActividades.append("Obligaciones del contratista:")
                texActividades.append("2.1 Verificar la calidad gr�fica y digital de los elementos, textos,formatos de productos cartogr�ficos obtenidos en el proyecto de mantenimiento de bases de datos, de acuerdo con las asignaciones del supervisor del proyecto.")
                texActividades.append("2.2 Verificar la consistencia tem�tica, consitencia l�gica, la cantidad de elementos, la correcta posici�n y ortograf�a de los textos y el correcto diligenciamiento del formato de salida gr�fica.")
                texActividades.append("2.3 Actualizar las bases impresas a partir de los archivos existentes de clasificaci�n de campo y toponimia.")
                texActividades.append("2.4 Elaborar el reporte por cada mapa y entregar las observaciones sobre cada uno de ellos.")
                texActividades.append("2.5 Documentar las actividades de acuerdo con los formatos establecidos por la subdirecci�n de geograf�a y cartograf�a cuando sea requerido.")
            elif Actividad=="Edicion":
                texActividades.append("Obligaciones del contratista:")
                texActividades.append("2.1 Realizar edici�n y estructuraci�n topol�gica de cada uno de los elementos contenidos en cada una de las hojas cartogr�ficas que le sean asignadas.")
                texActividades.append("2.2 Cargar los campos que sean requeridos conforme a la base de datos.")
                texActividades.append("2.3 Verificar la correcta estructuraci�n de los elementos, de acuerdo a lo establecido por la Subdirecci�n de Geograf�a y Cartograf�a.")
                texActividades.append("2.4 Verificar los empalmes digitales para cada una de las hojas, en cada uno de los elementos cartografiados.")
                texActividades.append("2.5 Verificar el correcto despliegue de la informaci�n transferida.")
                texActividades.append("2.6 Realizar el control de calidad de la informaci�n cartogr�fica obtenida a partir de los procesos de compilaci�n topon�mica, estructuraci�n base de datos para clasificaci�n de campo, \
                                      salidas gr�ficas preliminares y finales, seg�n especificaciones y manuales establecidos por la Subdirecci�n de Geograf�a y Cartograf�a.")
                texActividades.append("2.7 Garantizar la consistencia tem�tica, consistencia l�gica, la cantidad de elementos, la correcta posici�n y ortograf�a de los textos y el correcto diligenciamiento de los formatos establecidos para el control.")
                texActividades.append("2.8 Garantizar la calidad gr�fica de  los elementos, textos, formatos de productos cartogr�ficos a diferentes escalas elaborados por restituci�n fotogram�trica, de acuerdo con las asignaciones y plan del trabajo del �rea t�cnica.")
                texActividades.append("2.9 Aceptar y realizar las complementaciones de informaci�n necesarias para la aprobaci�n de las bases de datos cartogr�ficas, as� como las salidas gr�ficas seg�n corresponda el proceso.")
                texActividades.append("2.10 Verificar los empalmes digitales y gr�ficos para cada una de las hojas en cada uno de los lados que est� presente y para cada uno de los elementos cartografiados, seg�n los procesos asignados.")
                texActividades.append("2.12 Diligenciar los formatos que identifican y documentan el flujo de producci�n establecidos por la subdirecci�n, los cuales deben ir firmados, garantizando las actividades realizadas \
                                      sobre cada una de las hojas, el no cumplimiento de las actividades se�aladas en estos formatos o no documentaci�n de las mismas, implica la no facturaci�n de las hojas cartograficas trabajadas")
            elif Actividad=="Estandarizacion":
                texActividades.append("Obligaciones del contratista:")
                texActividades.append("2.1. Verificar consistencia tem�tica, l�gica, grado de totalidad, posici�n de los elementos, exactitud de atributos (incluye ortograf�a), consistencia de dominio y formato en los insumos para la generalizaci�n de cartograf�a b�sica.")
                texActividades.append("2.2 .Realizar revisi�n de clasificaci�n, empalmes y totalidad de los insumos requeridos para la generaci�n de cartograf�a b�sica.")
                texActividades.append("2.3. Cargar los campos que sean requeridos conforme a la base de datos.")
                texActividades.append("2.5 Verificar los empalmes digitales para cada una de las hojas, en cada uno de los elementos cartografiados.")
                texActividades.append("2.6 Verificar la calidad gr�fica y digital de los elementos, textos, formatos de productos cartogr�ficos obtenidos en el proceso de generaci�n de cartograf�a b�sica, de acuerdo con las asignadas del supervisor del proyecto.")
                texActividades.append("2.7 Realizar la transferencia de la informaci�n a los formatos digitales requeridos.")
            elif Actividad=="Metadato":
                texActividades.append("Obligaciones del contratista:")
                texActividades.append("2.1 Gestionar y complementar la documentaci�n de la cartograf�a actualizada a escala 1:25.000.")
                texActividades.append("2.2 Verificar los empalmes digitales para cada una de las hojas, en cada uno de los elementos cartografiados.")
                texActividades.append("2.3 Realizar la transferencia de informaci�n a los formatos digitales requeridos.")
                texActividades.append("2.4 Verificar el correcto despliegue de la informaci�n transferida.")
                texActividades.append("2.5 Desarrollar los ploteos requeridos para el desarrollo de otros procesos como para su respectiva revisi�n.")
                texActividades.append("2.6 Generar las salidas finales en papel de seguridad y/o pdf de acuerdo al formato establecido por el instituto para cada escala.")
                texActividades.append("2.7 Diligenciar los formatos de metadatos y memoria t�cnica correspondiente a cada una de las hojas cartogr�ficas efectuadas y por proyecto, de acuerdo a lo establecido por la subdirecci�n de geograf�a y cartograf�a.")
            return texActividades


        for text in actividades(ActividadContractual):
            para = Paragraph(text, styles["Justify"])
            elements.append(para)
        # espacio adicional
        elements.append(Spacer(0, inch*.2))

        t=Table(data,colWidths=[7 * cm, 3 * cm, 2 * cm,2* cm, 2 * cm],rowHeights = [1.3*cm]* len(data),
                        style=[
                        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                        ('FONT', (0,0),(4,0),'Helvetica-Bold',12),
                        ('FONTSIZE', (0,0), (-1, -1),6),
                        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                         ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                        ])
        elements.append(t)

        Sumatorias =Paragraph("<strong>Valor Total: %s</strong> "%(str(round(suma(tablaEstadisticas,"SUM_VALOR_PAGADO"),2))),styles["Right"])
        elements.append(Spacer(0, inch*.1))
        elements.append(Sumatorias)
        elements.append(Spacer(0, inch*.5))
        print str(valorUnico(tablaEntrada,"CONTRATISTA"))
        firma= ["Nombre del Contratista: %s"%(str(valorUnico(tablaEntrada,"CONTRATISTA"))),"Vo.Bo Supervisor: ______________________________"]
        firmaCotratista=["Firma: ______________________________  "," Vo.Bo Interventor: ______________________________  "]
        footer=[]
        footer.append(firma)
        footer.append(firmaCotratista)

        t=Table(footer,style=[
                        ('BOX', (0,0), (-1,-1), 0.25, colors.white),
                        ('FONTSIZE', (0,0), (-1, -1),7),
                        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.white),
                        ])
        elements.append(t)
        doc.build(elements)
        del doc
        del data
        arcpy.Delete_management("in_memory\TablaEstadisticas")
    except Exception as e:
        arcpy.AddMessage("Error Creando PDF " + e.message)
else:
    arcpy.AddMessage("Debe realizar un Query o una seleccion a la tabla, Intentelo de nuevo")

