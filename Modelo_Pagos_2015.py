#!/usr/bin/python
# -*- coding: ISO-8859-1 -*-

__author__ = 'fernando.gonzalez'
import arcpy,sys,os

arcpy.CreatePersonalGDB_management(r"X:\PRUEBAS\Reporte_Pagos_2016","Pagos.mdb")
Geodatabase =r"X:\PRUEBAS\Reporte_Pagos_2016"+os.sep+"Pagos.mdb"
#Tablas
Control_Calidad=arcpy.CreateTable_management(Geodatabase,"PAGOS_CONTROL_CALIDAD_V1")
Edicion=arcpy.CreateTable_management(Geodatabase,"PAGOS_EDICION_V1")
Control_Captura=arcpy.CreateTable_management(Geodatabase,"PAGOS_CONTROL_CAPTURA_DTM_V1")
Mantenimiento_Bases=arcpy.CreateTable_management(Geodatabase,"PAGOS_MANTENIMIENTO_BASES_V1")


arcpy.AddMessage("Creando Campos Control Calidad....")

arcpy.AddField_management(Control_Calidad,"PROYECTO_PLANCHA","TEXT","","","50","Indentificador Proyecto y Plancha")
arcpy.AddField_management(Control_Calidad,"PLANCHA","TEXT","","","20","Identificador de la Plancha")
arcpy.AddField_management(Control_Calidad,"CONTRATISTA","TEXT","","","255","Nombre del Contratista")
arcpy.AddField_management(Control_Calidad,"PROYECTO","TEXT","","","50","Proyecto al que corresponde la plancha")
arcpy.AddField_management(Control_Calidad,"ACTIVIDAD","TEXT","","","100","Actividad del Contrato")
arcpy.AddField_management(Control_Calidad,"ESCALA","TEXT","","","20","Escala de la plancha reportada")
arcpy.AddField_management(Control_Calidad,"UNIDAD_MEDICION","TEXT","","","30","Unidad de Medicion de la actividad")
arcpy.AddField_management(Control_Calidad,"NUMERO_UNIDADES","DOUBLE","","","","Número de unidades reportada")
arcpy.AddField_management(Control_Calidad,"AREA_PLANCHA","DOUBLE","","","","Area en Hectareas de la Plancha")
arcpy.AddField_management(Control_Calidad,"VALOR_ACTIVIDAD","DOUBLE","","","","Valor en pesos de la actividad")

arcpy.AddMessage("Creando Campos Edicion....")

arcpy.AddField_management(Edicion,"PROYECTO_PLANCHA","TEXT","","","50","Indentificador Proyecto y Plancha")
arcpy.AddField_management(Edicion,"PLANCHA","TEXT","","","20","Identificador de la Plancha")
arcpy.AddField_management(Control_Calidad,"CONTRATISTA","TEXT","","","255","Nombre del Contratista")
arcpy.AddField_management(Edicion,"PROYECTO","TEXT","","","50","Proyecto al que corresponde la plancha")
arcpy.AddField_management(Edicion,"ACTIVIDAD","TEXT","","","100","Actividad del Contrato")
arcpy.AddField_management(Edicion,"ESCALA","TEXT","","","20","Escala de la plancha reportada")
arcpy.AddField_management(Edicion,"UNIDAD_MEDICION","TEXT","","","30","Unidad de Medicion de la actividad")
arcpy.AddField_management(Edicion,"NUMERO_UNIDADES","DOUBLE","","","","Numero de unidades reportada")
arcpy.AddField_management(Edicion,"AREA_PLANCHA","DOUBLE","","","","Area en Hectareas de la Plancha")
arcpy.AddField_management(Edicion,"VALOR_ACTIVIDAD","DOUBLE","","","","Valor en pesos de la actividad")

arcpy.AddMessage("Creando Campos Control Captura...")

arcpy.AddField_management(Control_Captura,"PROYECTO_PLANCHA","TEXT","","","50","Indentificador Proyecto y Plancha")
arcpy.AddField_management(Control_Captura,"PLANCHA","TEXT","","","20","Identificador de la Plancha")
arcpy.AddField_management(Control_Calidad,"CONTRATISTA","TEXT","","","255","Nombre del Contratista")
arcpy.AddField_management(Control_Captura,"PROYECTO","TEXT","","","50","Proyecto al que corresponde la plancha")
arcpy.AddField_management(Control_Captura,"ACTIVIDAD","TEXT","","","100","Actividad del Contrato")
arcpy.AddField_management(Control_Captura,"ESCALA","TEXT","","","20","Escala de la plancha reportada")
arcpy.AddField_management(Control_Captura,"UNIDAD_MEDICION","TEXT","","","30","Unidad de Medición de la actividad")
arcpy.AddField_management(Control_Captura,"NUMERO_UNIDADES","DOUBLE","","","","Numero de unidades reportada")
arcpy.AddField_management(Control_Captura,"AREA_PLANCHA","DOUBLE","","","","Area en Hectareas de la Plancha")
arcpy.AddField_management(Control_Captura,"VALOR_ACTIVIDAD","DOUBLE","","","","Valor en pesos de la actividad")

arcpy.AddMessage("Creando Campos Mantenimiento de Bases....")

arcpy.AddField_management(Mantenimiento_Bases,"PROYECTO_PLANCHA","TEXT","","","50","Indentificador Proyecto y Plancha")
arcpy.AddField_management(Mantenimiento_Bases,"PLANCHA","TEXT","","","20","Identificador de la Plancha")
arcpy.AddField_management(Control_Calidad,"CONTRATISTA","TEXT","","","255","Nombre del Contratista")
arcpy.AddField_management(Mantenimiento_Bases,"PROYECTO","TEXT","","","50","Proyecto al que corresponde la plancha")
arcpy.AddField_management(Mantenimiento_Bases,"ACTIVIDAD","TEXT","","","100","Actividad del Contrato")
arcpy.AddField_management(Mantenimiento_Bases,"ESCALA","TEXT","","","20","Escala de la plancha reportada")
arcpy.AddField_management(Mantenimiento_Bases,"UNIDAD_MEDICION","TEXT","","","30","Unidad de Medición de la actividad")
arcpy.AddField_management(Mantenimiento_Bases,"NUMERO_UNIDADES","DOUBLE","","","","Número de unidades reportada")
arcpy.AddField_management(Mantenimiento_Bases,"AREA_PLANCHA","DOUBLE","","","","Area en Hectareas de la Plancha")
arcpy.AddField_management(Mantenimiento_Bases,"VALOR_ACTIVIDAD","DOUBLE","","","","Valor en pesos de la actividad")


#Creacion de Dominios
arcpy.env.workspace=r"X:\PRUEBAS\Reporte_Pagos_2016\DOMINIOS.mdb"
listaTablas = arcpy.ListTables()

for tabla in listaTablas:
    arcpy.AddMessage("creando dominio: "+ tabla)
    arcpy.TableToDomain_management(tabla,"codigo","descripción",Geodatabase,tabla)
    if tabla == "Dom_Actividades_Pagos_CC":
        arcpy.AssignDomainToField_management(Control_Calidad,"ACTIVIDAD",tabla)
    elif tabla == "Dom_Actividades_Pagos_ED":
        arcpy.AssignDomainToField_management(Edicion,"ACTIVIDAD",tabla)
    elif tabla == "Dom_Actividades_Pagos_MA":
        arcpy.AssignDomainToField_management(Mantenimiento_Bases,"ACTIVIDAD",tabla)
    elif tabla == "Dom_Actividades_Pagos_RE":
        arcpy.AssignDomainToField_management(Control_Captura,"ACTIVIDAD",tabla)
    elif tabla == "Dom_Escala_Pagos":
        arcpy.AssignDomainToField_management(Control_Calidad,"ESCALA",tabla)
        arcpy.AssignDomainToField_management(Edicion,"ESCALA",tabla)
        arcpy.AssignDomainToField_management(Control_Captura,"ESCALA",tabla)
        arcpy.AssignDomainToField_management(Mantenimiento_Bases,"ESCALA",tabla)
    elif tabla == "Dom_Unidad_Medicion":
        arcpy.AssignDomainToField_management(Control_Calidad,"UNIDAD_MEDICION",tabla)
        arcpy.AssignDomainToField_management(Edicion,"UNIDAD_MEDICION",tabla)
        arcpy.AssignDomainToField_management(Control_Captura,"UNIDAD_MEDICION",tabla)
        arcpy.AssignDomainToField_management(Mantenimiento_Bases,"UNIDAD_MEDICION",tabla)
    elif tabla == "Dom_Proyecto_2016":
        arcpy.AssignDomainToField_management(Control_Calidad,"PROYECTO",tabla)
        arcpy.AssignDomainToField_management(Edicion,"PROYECTO",tabla)
        arcpy.AssignDomainToField_management(Control_Captura,"PROYECTO",tabla)
        arcpy.AssignDomainToField_management(Mantenimiento_Bases,"PROYECTO",tabla)


