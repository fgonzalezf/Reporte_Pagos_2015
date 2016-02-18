__author__ = 'fernando.gonzalez'
import arcpy,sys,os

arcpy.CreatePersonalGDB_management(r"X:\PRUEBAS\Reporte_Pagos_2016","Pagos.mdb")
Geodatabase =r"X:\PRUEBAS\Reporte_Pagos_2016"+os.sep+"Pagos.mdb"
#Tablas
arcpy.CreateTable_management(Geodatabase,"CCB_PAGOS")
arcpy.CreateTable_management(Geodatabase,"CCB_PAGOS")
arcpy.CreateTable_management(Geodatabase,"CCB_PAGOS")
arcpy.CreateTable_management(Geodatabase,"CCB_PAGOS")
arcpy.CreateTable_management(Geodatabase,"CCB_PAGOS")

