__author__ = 'fernando.gonzalez'
import arcpy, os, sys
# importar utf8
reload(sys)
sys.setdefaultencoding("utf-8")
#Parametros

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

def TablaArray(table):
        array=[]
        rows = arcpy.SearchCursor(table)
        listFields = arcpy.ListFields(table)
        for row in rows:
            arrayrow=[]
            for field in listFields:
                arrayrow.append(row.getValue(field.name))
            array.append(arrayrow)
        return array

camposSum= [["AREA","SUM"],["VALOR_PAGADO","SUM"]]
camposUnicos= ["ESCALA","ACTIVIDAD","CONTRATISTA"]

arcpy.Statistics_analysis(tablaEntrada, tablaEstadisticas, camposSum, camposUnicos)
calcularDescripcion(tablaEstadisticas,"DOM_PAGOS_ESCALA","ESCALA")
calcularDescripcion(tablaEstadisticas,"Dom_Actividad_Pagos","ACTIVIDAD")

data=TablaArray(tablaEstadisticas)

from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
width, height = letter
doc = SimpleDocTemplate("X:\PRUEBAS\PDF\simple_table_grid3.pdf", pagesize=letter)
elements = []
t=Table(data,style=[('GRID',(1,1),(-2,-2),1,colors.black),
                ('BOX',(0,0),(1,-1),2,colors.black),
                ('LINEABOVE',(1,2),(-2,2),1,colors.black),
                ('FONTSIZE',(5)),
                ('LINEBEFORE',(2,1),(2,-2),1,colors.black),
                ])

elements.append(t)
doc.build(elements)
