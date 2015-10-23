# -*- coding: utf-8 -*-
__author__ = 'fernando.gonzalez'
import os
import sys
import arcpy
import datetime
# importar utf8
reload(sys)
sys.setdefaultencoding("utf-8")
#Parametros
arcpy.env.overwriteOutput=True
tablaEntrada=r"X:\PRUEBAS\ReportePagos_2015\Datos_Prueba.gdb\DATOS_PRUEBA"
tablaEstadisticas=r"X:\PRUEBAS\ReportePagos_2015\Datos_Prueba.gdb\Estadisticas"


def calcularDescripcion(tabla,dominio,campo):
    arcpy.DomainToTable_management(os.path.dirname(tablaEntrada),dominio,"in_memory/dominioOut","codigo","descripcion")
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

def TablaArray(table,fields):
        array=[]
        rows = arcpy.SearchCursor(table)
        encabezado=[]
        for field in fields:
            if field == "ACTIVIDAD":
                encabezado.append("Actividad Relacionada Segun Contrato")
            if field == "SUM_AREA":
                encabezado.append("Area HA")
            if field == "SUM_AREA":
                encabezado.append("Area HA")

        array.append(field)
        for row in rows:
            arrayrow=[]
            for field in fields:
                arrayrow.append(row.getValue(field))
            array.append(arrayrow)
        return array

camposSum= [["AREA","SUM"],["VALOR_PAGADO","SUM"]]
camposUnicos= ["ESCALA","ACTIVIDAD","PROYECTO"]
fields=["ACTIVIDAD","PROYECTO","ESCALA","SUM_AREA","SUM_VALOR_PAGADO"]
arcpy.Statistics_analysis(tablaEntrada, tablaEstadisticas, camposSum, camposUnicos)
calcularDescripcion(tablaEstadisticas,"DOM_PAGOS_ESCALA","ESCALA")
calcularDescripcion(tablaEstadisticas,"Dom_Actividad_Pagos","ACTIVIDAD")
calcularDescripcion(tablaEstadisticas,"Dom_Proyecto_Pagos","PROYECTO")

data=TablaArray(tablaEstadisticas,fields)

from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER,TA_JUSTIFY,TA_LEFT,TA_RIGHT
from reportlab.lib.units import inch
from reportlab.lib import colors


####################
width, height = letter
doc = SimpleDocTemplate("X:\PRUEBAS\PDF\simple_table_grid24.pdf", pagesize=letter)
elements = []
#Alineacion

styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
styles.add(ParagraphStyle(name='Left', alignment=TA_LEFT))
styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))
styles.add(ParagraphStyle(name='Right', alignment=TA_RIGHT))

# FECHA

fecha= datetime.date.today()
hoy= "Bogotá "+fecha.strftime("%d/%m/%Y")

fechapara=Paragraph(hoy, styles["Left"])
elements.append(fechapara)

elements.append(Spacer(0, inch*.3))

# creamos título con estilo
titulo = Paragraph("INFORME DE PRODUCCIÓN",styles["Center"])
elements.append(titulo)
# Contrato
contrato = "12245-2013"
contratotxt = Paragraph("CONTRATO No. <strong>%s</strong>"%(contrato),styles["Center"])
elements.append(contratotxt)
#Periodo
periodo = "2015-01-01 al 2015-02-01"
periodotxt=Paragraph("Periódo a Reportar <strong>%s</strong>"%(periodo),styles["Center"])
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
        texActividades.append("2.3- Diligenciar los formatos respectivos del control  del control de calidad realizando a cada proyecto.")
        texActividades.append("2.4- Cumplir con los rendimientos en producción establecidos por la subdirección de geografía y cartografía.")
        texActividades.append("2.5- Realizar el diagnostico de cada hoja cartográfica asignada y aceptarla si cumple con el 90% de las especificaciones.")
    return texActividades


for text in actividades("Control Restitucion"):
    para = Paragraph(text, styles["Justify"])
    elements.append(para)


# espacio adicional
elements.append(Spacer(0, inch*.2))




t=Table(data,style=[
                ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                ('FONTSIZE', (0,0), (-1, -1),4),
                ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                ])

elements.append(t)
doc.build(elements)
