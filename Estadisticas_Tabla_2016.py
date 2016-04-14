#!/usr/bin/python
# -*- coding: latin-1 -*-

import os
import sys
import arcpy
import datetime
reload(sys)
sys.setdefaultencoding("iso-8859-1")

from reportlab.lib.pagesizes import letter, cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER,TA_JUSTIFY,TA_LEFT,TA_RIGHT
from reportlab.lib.units import inch
from reportlab.lib import colors

styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, fontSize=8))
styles.add(ParagraphStyle(name='Left', alignment=TA_LEFT, fontSize=8))
styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER, fontSize=8))
styles.add(ParagraphStyle(name='Center_Table', alignment=TA_CENTER, fontSize=6.5,leading=7.5))
styles.add(ParagraphStyle(name='Right', alignment=TA_RIGHT, fontSize=8))
styles.add(ParagraphStyle(name='Tabla', alignment=TA_LEFT, fontSize=6,leading=6.5))

#importar utf8
#Parametros
arcpy.env.overwriteOutput=True
#tablaEntrada=r"X:\PRUEBAS\Reporte_Pagos_2016\PRUEBAS\Pagos_V3.mdb\PAGOS_EDICION_V1"
#tablaEstadisticas="in_memory\TablaEstadisticas"
#ActividadContractual="Edicion"
#reportarPeriodo="true"
#pdfSalida =r"X:\PRUEBAS\Reporte_Pagos_2016\PRUEBAS\prueba2.pdf"
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




def CrearConexionPagos():
    RutaGDB= os.getenv('APPDATA')+ os.sep+"conexion.sde"
    if arcpy.Exists(RutaGDB)==False:
        arcpy.CreateArcSDEConnectionFile_management(os.getenv('APPDATA'),
                                            "conexion.sde",
                                            "172.17.2.247",
                                            '5151',
                                            '',
                                            "DATABASE_AUTH",
                                            'PAGOS',
                                            'PagosGitPc',
                                            'SAVE_USERNAME',
                                            'SDE.DEFAULT',
                                            'SAVE_VERSION')
    return RutaGDB

def calcularDescripcion(tabla,dominio,campo):
    try:
        workspace=CrearConexionPagos()
        arcpy.DomainToTable_management(workspace,dominio,"in_memory/dominioOut","codigo","descripcion")
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
                encabezado.append(Paragraph(latin1toUTF8("<B>Actividades Relacionadas según Contrato</B>"),styles["Center_Table"]))
            elif field == "SUM_NUMERO_UNIDADES":
                encabezado.append(Paragraph("<B>No Unidades</B>",styles["Center_Table"]))
            elif field == "SUM_VALOR_ACTIVIDAD":
                encabezado.append(Paragraph("<B>Valor</B>",styles["Center_Table"]))
            elif field == "UNIDAD_MEDICION":
                encabezado.append(Paragraph(latin1toUTF8("<B>Unidad Medición</B>"),styles["Center_Table"]))
            else:
                encabezado.append(Paragraph("<B>"+field.title()+"</B>",styles["Center_Table"]))
        array.append(encabezado)
        #print encabezado
        for row in rows:
            arrayrow=[]
            for field in fields:
                if row.getValue(field)==None:
                    arrayrow.append(Paragraph("",styles["Tabla"]))
                else:
                    arrayrow.append(Paragraph(latin1toUTF82(str(row.getValue(field))),styles["Tabla"]))
            array.append(arrayrow)
        return array
    except Exception as e:
        arcpy.AddMessage(e.message)
        #return array

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

def DominioCampo(Tabla,Campo):
    fields = arcpy.ListFields(Tabla)
    dominio=""
    for field in fields:
        if field.name ==Campo:
            dominio= field.domain
    return dominio
def latin1toUTF8(s):
    if s==None:
        return ""
    else:
        return unicode(s, "iso-8859-1").encode("iso-8859-1")
def latin1toUTF82(s):
    if s==None:
        return ""
    else:
        return unicode(s, "iso-8859-1").encode("utf-8")

def validarCompletitud (tabla):
    fields=arcpy.ListFields(tabla)
    completo=[True,"",""]
    for field in fields:

        if field.name!="OBSERVACIONES" and completo[0]==True :
            #print field.name
            rows=arcpy.SearchCursor(tabla)
            for row in rows:
                #print row.getValue(field.name)
                if row.getValue(field.name)== None:
                    completo[0]=False
                    completo[1]=field.name
                    completo[2]=row.getValue("OBJECTID")
                    break
        else:
            break
    return completo




result = int(arcpy.GetCount_management(tablaEntrada).getOutput(0))
validacion=validarCompletitud(tablaEntrada)
#print(str(validacion[0]) + "  "+ validacion[1])
if result<2000 and validacion[0]==True:
    try:

        camposSum= [["NUMERO_UNIDADES","SUM"],["VALOR_ACTIVIDAD","SUM"]]
        camposUnicos= ["ESCALA","ACTIVIDAD","PROYECTO","UNIDAD_MEDICION","CONTRATISTA"]
        fields=["ACTIVIDAD","PROYECTO","ESCALA","UNIDAD_MEDICION","SUM_NUMERO_UNIDADES","SUM_VALOR_ACTIVIDAD"]
        arcpy.Statistics_analysis(tablaEntrada, tablaEstadisticas, camposSum, camposUnicos)
        #Dominio Contratista
        contratista=""
        try:
            dom = DominioCampo(tablaEntrada,"CONTRATISTA")
            calcularDescripcion(tablaEstadisticas,dom,"CONTRATISTA")
            contratista=str(valorUnico(tablaEstadisticas,"CONTRATISTA"))
            arcpy.AddMessage("El contratista es: "+contratista)
            arcpy.DeleteField_management(tablaEstadisticas,"CONTRATISTA")

        except  Exception as e:
            arcpy.AddMessage("Error Calculando dominio Contratista..." + e.message)

        try:
            dom = DominioCampo(tablaEntrada,"ACTIVIDAD")
            calcularDescripcion(tablaEstadisticas,dom,"ACTIVIDAD")

        except  Exception as e:
            arcpy.AddMessage("Error Calculando dominio Contratista..." + e.message)

        calcularDescripcion(tablaEstadisticas,"Dom_Escala_Pagos","ESCALA")
        calcularDescripcion(tablaEstadisticas,"Dom_Proyecto_2016","PROYECTO")
        calcularDescripcion(tablaEstadisticas,"Dom_Unidad_Medicion","UNIDAD_MEDICION")
        arcpy.AddMessage("Convirtiendo tabla")
        data=TablaArray(tablaEstadisticas,fields)
        #print str(validacion[0])
        ##Formateo de Actividad y Proyecto
        arcpy.AddMessage("Tabla convertida")
        ####################
        width, height = letter
        doc = SimpleDocTemplate(pdfSalida, pagesize=letter,rightMargin=51,leftMargin=51,topMargin=50,bottomMargin=18)
        elements = []
        #Alineacion
        # FECHA
        fecha= datetime.date.today()
        hoy= "Bogotá "+fecha.strftime("%d/%m/%Y")

        fechapara=Paragraph(latin1toUTF8(hoy), styles["Left"])
        elements.append(fechapara)

        elements.append(Spacer(0, inch*.2))

        # creamos título con estilo
        titulo = Paragraph(latin1toUTF8("INFORME DE PRODUCCIÓN"),styles["Center"])
        elements.append(titulo)
        # Contrato
        contratotxt = Paragraph("CONTRATO No. <strong>%s</strong>"%(NoContrato),styles["Center"])
        elements.append(contratotxt)
        #Periodo
        if reportarPeriodo=="true":
            periodotxt=Paragraph(latin1toUTF8("Periódo a Reportar <strong>%s</strong>"%(periodo)),styles["Center"])
            elements.append(periodotxt)
        elements.append(Spacer(0, inch*.3))

        actividadesTitulo =Paragraph("<strong>ACTIVIDADES DEL CONTRATO</strong>",styles["Right"])
        # espacio adicional
        elements.append(Spacer(0, inch*.1))

        def actividades(Actividad):
            texActividades=[]
            if Actividad=="Control Restitucion":
                texActividades.append("Obligaciones del contratista:")
                texActividades.append("2.1- Validar en estación digital la correcta captura de los elementos altimétricos y planimétricos o modelos digitales del terreno,obtenidos mediante restitución \
                                       por funcionarios y contratistas del área, a diferentes escalas, de acuerdo con las asignaciones y plan del trabajo del área técnica.")
                texActividades.append("2.2- Verificar la consistencia temática, consistencia lógica, la totalidad de la información. La correcta posición y los empalmes y conectividad entre niveles.")
                texActividades.append("2.3- Diligenciar los formatos respectivos del control de calidad realizado a cada proyecto.")

            elif Actividad=="Control Calidad Digital":
                texActividades.append("Obligaciones del contratista:")
                texActividades.append("2.1 Realizar el diagnóstico general y evaluar la calidad de la información cartográfica digital producida por actualización de las hojas cartográficas a las diferentes escalas de producción.")
                texActividades.append("2.2 Realizar el control de estandarización de la información para lo cual la contratista debe revisar el grado de totalidad, consistencia lógica, consistencia temática, exactitud en posición,\
                                        de la información digital de acuerdo con el catalogo de objetos y el modelo de datos IGAC y comprobar que sean efectuadas las correcciones solicitadas a los procesos de edición y estructuración,\
                                        elaborar los metadatos correspondientes a cada una de las planchas efectuadas.")
                texActividades.append("2.3 Realizar los complementos y ajustes necesarios que resulten del control digital y de los procesos de revisión y control de calidad y los lineamientos del coordinador del proyecto.")
                texActividades.append("2.4 Diligenciar y documentar las actividades de acuerdo con los formatos establecidos por la subdirección de geografía y cartografía.")
                texActividades.append("2.12 Verificar los empalmes para cada una de las hojas en cada uno de los lados que esta  presente y para cada uno de los elementos cartograficos.")
            elif Actividad=="Mantenimiento":
                texActividades.append("Obligaciones del contratista:")
                texActividades.append("2.1 Cumplir con el plan de trabajo establecido para el objecto a desarrollar.")
                texActividades.append("2.2 Realizar la captura de los elementos planimétricos conforme a las tolerancias para la escala, a partir de imágenes \
                                        ópticas y de radar necesarias para el mantenimiento de las bases de datos cartograficas de la subdirección de geografia y cartografia.")
                texActividades.append("2.4 Actualizar las salidas gráficas convencionales de acuerdo con el formato aprobado para tal fin.")
                texActividades.append("2.5 Realizar las salidas gráficas de mapa plegado de acuerdo con el formato aprobado para tal fin.")
                texActividades.append("2.6 Edición de toponimia conforme a los requerimientos definido para la base de datos multiescala.")
            elif Actividad=="Control Actualizacion":
                texActividades.append("Obligaciones del contratista:")
                texActividades.append("2.1 Realizar el diagnóstico general y evaluar la calidad de la información cartográfica digital producida por actualización de las hojas cartográficas a las diferentes escalas de producción.")
                texActividades.append("2.2 Realizar el control de estandarización de la información para lo cual el contratista debe revisar el grado de totalidad, consistencia lógica, consistencia temática, exactitud en posición, \
                                        de la información digital de acuerdo con el catálogo de objetos y el modelo de datos IGAC y comprobar que sean efectuadas las correcciones solicitadas a los procesos de edición, \
                                        digitalización y estructuración, elaborar los metadatos correspondientes a cada una de las planchas efectuadas.")
                texActividades.append("2.3 Realizar los complementos y ajustes necesarios que resulten del control digital y de los procesos de revisión y control de calidad y los lineamientos del coordinador del proyecto.")
                texActividades.append("2.5 Diligenciar y documentar las actividades de acuerdo con los formatos establecidos por la subdirección de geografía y cartografía.")
            elif Actividad=="Control Calidad Grafico":
                texActividades.append("Obligaciones del contratista:")
                texActividades.append("2.1 Verificar la calidad gráfica y digital de los elementos, textos,formatos de productos cartográficos obtenidos en el proyecto de mantenimiento de bases de datos, de acuerdo con las asignaciones del supervisor del proyecto.")
                texActividades.append("2.2 Verificar la consistencia temática, consitencia lógica, la cantidad de elementos, la correcta posición y ortografía de los textos y el correcto diligenciamiento del formato de salida gráfica.")
                texActividades.append("2.3 Actualizar las bases impresas a partir de los archivos existentes de clasificación de campo y toponimia.")
                texActividades.append("2.4 Elaborar el reporte por cada mapa y entregar las observaciones sobre cada uno de ellos.")
                texActividades.append("2.5 Documentar las actividades de acuerdo con los formatos establecidos por la subdirección de geografía y cartografía cuando sea requerido.")
            elif Actividad=="Edicion":
                texActividades.append("Obligaciones del contratista:")
                texActividades.append("2.1 Realizar edición y estructuración topológica de cada uno de los elementos contenidos en cada una de las hojas cartográficas que le sean asignadas.")
                texActividades.append("2.2 Cargar los campos que sean requeridos conforme al modelo de datos.")
                #texActividades.append("2.3 Verificar la correcta estructuración de los elementos, de acuerdo a lo establecido por la Subdirección de Geografía y Cartografía.")
                #texActividades.append("2.4 Verificar los empalmes digitales para cada una de las hojas, en cada uno de los elementos cartografiados.")
                texActividades.append("2.5 Verificar el correcto despliegue de la información transferida.")
                #texActividades.append("2.6 Garantizar la consistencia tema")
                texActividades.append("2.6 Garantizar la consistencia temática, consistencia lógica, la cantidad de elementos, la correcta posición y ortografía de los textos y el correcto diligenciamiento de los formatos establecidos para el control.")
                #texActividades.append("2.8 Garantizar la calidad gráfica de  los elementos, textos, formatos de productos cartográficos a diferentes escalas elaborados por restitución fotogramétrica, de acuerdo con las asignaciones y plan del trabajo del área técnica.")
                texActividades.append("2.8 Verificar los empalmes digitales y gráficos para cada una de las hojas en cada uno de los lados que está presente y para cada uno de los elementos cartografiados, según los procesos asignados.")
                texActividades.append("2.11 Cumplir con las especificaciones técnicas de productos asignados, de lo contrario constituira incumplimiento del contrato.")
                texActividades.append("2.12 Generar alertas al supervisor sobre inconsistencias presentes en las hojas adyacentes de los respectivos bloques asignados (definido el bloque como la hoja a trabajar junto con sus cuatro hojas de empalme)")
                texActividades.append("2.14 Corregir las inconsistencias que se encuentren en el producto entregado, definidos por el control de calidad.")
                texActividades.append("2.19 Verificar actividades según tablas de pagos.")
            elif Actividad=="Estandarizacion":
                texActividades.append("Obligaciones del contratista:")
                texActividades.append("2.1. Verificar consistencia temática, lógica, grado de totalidad, posición de los elementos, exactitud de atributos (incluye ortografía), consistencia de dominio y formato en los insumos para la generalización de cartografía básica.")
                texActividades.append("2.2 .Realizar revisión de clasificación, empalmes y totalidad de los insumos requeridos para la generación de cartografía básica.")
                texActividades.append("2.3. Cargar los campos que sean requeridos conforme a la base de datos.")
                texActividades.append("2.5 Verificar los empalmes digitales para cada una de las hojas, en cada uno de los elementos cartografiados.")
                texActividades.append("2.6 Verificar la calidad gráfica y digital de los elementos, textos, formatos de productos cartográficos obtenidos en el proceso de generación de cartografía básica, de acuerdo con las asignadas del supervisor del proyecto.")
                texActividades.append("2.7 Realizar la transferencia de la información a los formatos digitales requeridos.")
            elif Actividad=="Metadato":
                texActividades.append("Obligaciones del contratista:")
                texActividades.append("2.1 Gestionar y complementar la documentación de la cartografía actualizada a escala 1:25.000.")
                texActividades.append("2.2 Verificar los empalmes digitales para cada una de las hojas, en cada uno de los elementos cartografiados.")
                texActividades.append("2.3 Realizar la transferencia de información a los formatos digitales requeridos.")
                texActividades.append("2.4 Verificar el correcto despliegue de la información transferida.")
                texActividades.append("2.5 Desarrollar los ploteos requeridos para el desarrollo de otros procesos como para su respectiva revisión.")
                texActividades.append("2.6 Generar las salidas finales en papel de seguridad y/o pdf de acuerdo al formato establecido por el instituto para cada escala.")
                texActividades.append("2.7 Diligenciar los formatos de metadatos y memoria técnica correspondiente a cada una de las hojas cartográficas efectuadas y por proyecto, de acuerdo a lo establecido por la subdirección de geografía y cartografía.")
            elif Actividad=="Control Calidad Profesional":
                texActividades.append("Obligaciones del contratista:")
                texActividades.append("2.1 Verificar la calidad de los productos cartográficos, ortoimagen, compilación toponímica, base de datos cartográficas, salidas graficas preliminares y finales elaborados por los procesos de generación, actualización,\
                                      generalización y mantenimiento de hojas cartográficas,  de acuerdo con las asignaciones y tablas de pagos establecidos.")
                texActividades.append("2.2 Verificar la completitud de la captura a partir de imágenes satelitales, de acuerdo con el modelo de datos para la escala.")
                texActividades.append("2.3 Realizar el diagnóstico de cada hoja cartográfica asignada y aceptarla si cumple con los parámetros de calidad en las especificaciones.")
                texActividades.append("2.4 Realizar las complementaciones de información necesarias para la aprobación de las bases de datos cartográficas,así como las salidas gráficas según corresponda \
                                          el proceso y asignación del supervisor.")
                texActividades.append("2.7 Realizar la devolución de productos a su respectivo proveedor cuando no cumpla con los parámetros de calidad definidos en la especificación técnica.")
                texActividades.append("2.9 Generar alertas al supervisor sobre inconsistencias presentes en las hojas adyacentes de los respectivos bloques asignados (definido el bloque como la hoja a trabajar junto con sus cuatro hojas de empalme)")
                texActividades.append("2.11 Realizar los complementos y ajustes necesarios que resulten de los procesos de revisión y lineamientos del supervisor del proyecto.")
                texActividades.append("2.14 Verificar los empalmes digitales y gráficos para cada una de las hojas en cada uno de los lados que está  presente y para cada uno de los elementos cartografiados, según los procesos asignados.")
            elif Actividad=="Control Calidad Tecnico":
                texActividades.append("2.1 Diagnosticar cada hoja cartográfica asignada y aceptarla si cumple con los parámetros de calidad en las especificaciones.")
                texActividades.append("2.2 Realizar el control de calidad de los productos cartográficos, ortoimagen, compilación toponímica, base de datos cartográficas salidas gráfica preliminares y finales elaborados por los procesos de generación, \
                                       actualización generalización y mantenimiento de hojas cartográficas de acuerdo con las asignaciones y tablas  de pagos establecidos.")
                texActividades.append("2.4 Realizar las complementaciones de información necesarias para la aprobación de las bases de datos cartográficas,así como las salidas gráficas según corresponda \
                                          el proceso y asignación del supervisor.")
                texActividades.append("2.7 Realizar la devolución de productos a su respectivo proveedor cuando no cumpla con los parámetros de calidad definidos en la especificación técnica.")
                texActividades.append("2.9 Generar alertas al supervisor sobre inconsistencias presentes en las hojas adyacentes de los respectivos bloques asignados (definido el bloque como la hoja a trabajar junto con sus cuatro hojas de empalme)")
                texActividades.append("2.11 Realizar los complementos y ajustes necesarios que resulten de los procesos de revisión y lineamientos del supervisor del proyecto.")
                texActividades.append("2.14 Verificar los empalmes digitales y gráficos para cada una de las hojas en cada uno de los lados que está  presente y para cada uno de los elementos cartografiados, según los procesos asignados.")


            return texActividades


        for text in actividades(ActividadContractual):
            para = Paragraph(latin1toUTF8(text), styles["Justify"])
            elements.append(para)
        # espacio adicional
        elements.append(Spacer(0, inch*.2))

        t=Table(data,colWidths=[6.0 * cm, 3.5 * cm, 1.5 * cm,3* cm, 1.5 * cm, 2 * cm],rowHeights = [0.7*cm]* len(data),
                        style=[
                        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                        ('FONT', (0,0),(4,0),'Helvetica-Bold',10),
                        ('FONTSIZE', (0,0), (-1, -1),6),
                        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                         ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                        ])
        elements.append(t)

        Sumatorias =Paragraph("<strong>Valor Total: %s</strong> "%(str(round(suma(tablaEstadisticas,"SUM_VALOR_ACTIVIDAD"),2))),styles["Right"])
        elements.append(Spacer(0, inch*.1))
        elements.append(Sumatorias)
        elements.append(Spacer(0, inch*.4))
        #print str(valorUnico(tablaEntrada,"CONTRATISTA"))
        firma= ["Nombre del Contratista: %s"%(latin1toUTF82(contratista)),"Vo.Bo Supervisor: __________________________________"]
        firmaCotratista=["Firma: __________________________________  "," Vo.Bo Interventor: __________________________________  "]
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
    arcpy.AddWarning("...Celda Nula en el Campo: %s en el OBJECTID: %s..."%(validacion[1], validacion[2]) )
    arcpy.AddWarning("...La Tabla esta incompleta....")
    arcpy.AddWarning("...Complete la Tabla en todos los campos Obligatorios (Solo el Campo OBSERVACIONES es opcional....)")




