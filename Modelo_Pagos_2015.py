#!/usr/bin/python
# -*- coding: ISO-8859-1 -*-
__author__ = 'fernando.gonzalez'
import arcpy,sys,os

arcpy.CreatePersonalGDB_management(r"X:\PRUEBAS\Reporte_Pagos_2016","Pagos_V5.mdb","10.0")
Geodatabase =r"X:\PRUEBAS\Reporte_Pagos_2016"+os.sep+"Pagos_V5.mdb"
#Tablas
Control_Calidad=arcpy.CreateTable_management(Geodatabase,"PAGOS_CONTROL_CALIDAD_V1")
Edicion=arcpy.CreateTable_management(Geodatabase,"PAGOS_EDICION_V1")
Control_Captura=arcpy.CreateTable_management(Geodatabase,"PAGOS_CONTROL_CAPTURA_DTM_V1")
Mantenimiento_Bases=arcpy.CreateTable_management(Geodatabase,"PAGOS_MANTENIMIENTO_BASES_V1")
verificacion=arcpy.CreateTable_management(Geodatabase,"PAGOS_VERIFICACION_V1")


arcpy.AddMessage("Creando Campos Control Calidad....")

arcpy.AddField_management(Control_Calidad,"PROYECTO_PLANCHA","TEXT","","","50","")
arcpy.AddField_management(Control_Calidad,"PLANCHA","TEXT","","","20","")
arcpy.AddField_management(Control_Calidad,"CONTRATISTA","TEXT","","","255","")
arcpy.AddField_management(Control_Calidad,"PROYECTO","TEXT","","","50","")
arcpy.AddField_management(Control_Calidad,"ACTIVIDAD","TEXT","","","100","")
arcpy.AddField_management(Control_Calidad,"ESCALA","TEXT","","","20","")
arcpy.AddField_management(Control_Calidad,"NUMERO_ACTA","TEXT","","","2","")
arcpy.AddField_management(Control_Calidad,"CONTRATO","TEXT","","","50","")
arcpy.AddField_management(Control_Calidad,"UNIDAD_MEDICION","TEXT","","","30","")
arcpy.AddField_management(Control_Calidad,"NUMERO_UNIDADES","DOUBLE","","","","")
#arcpy.AddField_management(Control_Calidad,"AREA_PLANCHA","DOUBLE","","","","Area en Hectareas de la Plancha")
arcpy.AddField_management(Control_Calidad,"VALOR_ACTIVIDAD","DOUBLE","","","","")
arcpy.AddField_management(Control_Calidad,"FECHA","DATE","","","","")
arcpy.AddField_management(Control_Calidad,"APROBACION_SUPERVISOR","TEXT","","","2","")
arcpy.AddField_management(Control_Calidad,"ESTADO","TEXT","","","10","")
arcpy.AddField_management(Control_Calidad,"OBSERVACIONES","TEXT","","","255","")

arcpy.AddMessage("Creando Campos Edicion....")

arcpy.AddField_management(Edicion,"PROYECTO_PLANCHA","TEXT","","","50","")
arcpy.AddField_management(Edicion,"PLANCHA","TEXT","","","20","")
arcpy.AddField_management(Edicion,"CONTRATISTA","TEXT","","","255","")
arcpy.AddField_management(Edicion,"PROYECTO","TEXT","","","50","")
arcpy.AddField_management(Edicion,"ACTIVIDAD","TEXT","","","100","")
arcpy.AddField_management(Edicion,"ESCALA","TEXT","","","20","")
arcpy.AddField_management(Edicion,"NUMERO_ACTA","TEXT","","","2","")
arcpy.AddField_management(Edicion,"CONTRATO","TEXT","","","50","")
arcpy.AddField_management(Edicion,"UNIDAD_MEDICION","TEXT","","","30","")
arcpy.AddField_management(Edicion,"NUMERO_UNIDADES","DOUBLE","","","","")
#arcpy.AddField_management(Edicion,"AREA_PLANCHA","DOUBLE","","","","Area en Hectareas de la Plancha")
arcpy.AddField_management(Edicion,"VALOR_ACTIVIDAD","DOUBLE","","","","")
arcpy.AddField_management(Edicion,"FECHA","DATE","","","","")
arcpy.AddField_management(Edicion,"APROBACION_SUPERVISOR","TEXT","","","2","")
arcpy.AddField_management(Edicion,"ESTADO","TEXT","","","10","")
arcpy.AddField_management(Edicion,"OBSERVACIONES","TEXT","","","255","")
#contrato
#Fecha
#Aprobacion_Supervisor(si/no)

arcpy.AddMessage("Creando Campos Control Captura...")

arcpy.AddField_management(Control_Captura,"PROYECTO_PLANCHA","TEXT","","","50","")
arcpy.AddField_management(Control_Captura,"PLANCHA","TEXT","","","20","")
arcpy.AddField_management(Control_Captura,"CONTRATISTA","TEXT","","","255","")
arcpy.AddField_management(Control_Captura,"PROYECTO","TEXT","","","50","")
arcpy.AddField_management(Control_Captura,"ACTIVIDAD","TEXT","","","100","")
arcpy.AddField_management(Control_Captura,"ESCALA","TEXT","","","20","")
arcpy.AddField_management(Control_Captura,"NUMERO_ACTA","TEXT","","","2","")
arcpy.AddField_management(Control_Captura,"CONTRATO","TEXT","","","50","")
arcpy.AddField_management(Control_Captura,"UNIDAD_MEDICION","TEXT","","","30","")
arcpy.AddField_management(Control_Captura,"NUMERO_UNIDADES","DOUBLE","","","","")
#arcpy.AddField_management(Control_Captura,"AREA_PLANCHA","DOUBLE","","","","Area en Hectareas de la Plancha")
arcpy.AddField_management(Control_Captura,"VALOR_ACTIVIDAD","DOUBLE","","","","")
arcpy.AddField_management(Control_Captura,"FECHA","DATE","","","","")
arcpy.AddField_management(Control_Captura,"APROBACION_SUPERVISOR","TEXT","","","2","")
arcpy.AddField_management(Control_Captura,"ESTADO","TEXT","","","10","")
arcpy.AddField_management(Control_Captura,"OBSERVACIONES","TEXT","","","255","")

arcpy.AddMessage("Creando Campos Mantenimiento de Bases....")

arcpy.AddField_management(Mantenimiento_Bases,"PROYECTO_PLANCHA","TEXT","","","50","")
arcpy.AddField_management(Mantenimiento_Bases,"PLANCHA","TEXT","","","20","")
arcpy.AddField_management(Mantenimiento_Bases,"CONTRATISTA","TEXT","","","255","")
arcpy.AddField_management(Mantenimiento_Bases,"PROYECTO","TEXT","","","50","")
arcpy.AddField_management(Mantenimiento_Bases,"ACTIVIDAD","TEXT","","","100","")
arcpy.AddField_management(Mantenimiento_Bases,"ESCALA","TEXT","","","20","")
arcpy.AddField_management(Mantenimiento_Bases,"NUMERO_ACTA","TEXT","","","2","")
arcpy.AddField_management(Mantenimiento_Bases,"CONTRATO","TEXT","","","50","")
arcpy.AddField_management(Mantenimiento_Bases,"UNIDAD_MEDICION","TEXT","","","30","")
arcpy.AddField_management(Mantenimiento_Bases,"NUMERO_UNIDADES","DOUBLE","","","","")
#arcpy.AddField_management(Mantenimiento_Bases,"AREA_PLANCHA","DOUBLE","","","","Area en Hectareas de la Plancha")
arcpy.AddField_management(Mantenimiento_Bases,"VALOR_ACTIVIDAD","DOUBLE","","","","")
arcpy.AddField_management(Mantenimiento_Bases,"FECHA","DATE","","","","")
arcpy.AddField_management(Mantenimiento_Bases,"APROBACION_SUPERVISOR","TEXT","","","2","")
arcpy.AddField_management(Mantenimiento_Bases,"ESTADO","TEXT","","","10","")
arcpy.AddField_management(Mantenimiento_Bases,"OBSERVACIONES","TEXT","","","255","")

arcpy.AddMessage("Creando Campos Verificacion....")

arcpy.AddField_management(verificacion,"PROYECTO_PLANCHA","TEXT","","","50","")
arcpy.AddField_management(verificacion,"PLANCHA","TEXT","","","20","")
arcpy.AddField_management(verificacion,"CONTRATISTA","TEXT","","","255","")
arcpy.AddField_management(verificacion,"PROYECTO","TEXT","","","50","")
arcpy.AddField_management(verificacion,"ACTIVIDAD","TEXT","","","100","")
arcpy.AddField_management(verificacion,"ESCALA","TEXT","","","20","")
arcpy.AddField_management(verificacion,"NUMERO_ACTA","TEXT","","","2","")
arcpy.AddField_management(verificacion,"CONTRATO","TEXT","","","50","")
arcpy.AddField_management(verificacion,"UNIDAD_MEDICION","TEXT","","","30","")
arcpy.AddField_management(verificacion,"NUMERO_UNIDADES","DOUBLE","","","","")
#arcpy.AddField_management(Mantenimiento_Bases,"AREA_PLANCHA","DOUBLE","","","","Area en Hectareas de la Plancha")
arcpy.AddField_management(verificacion,"VALOR_ACTIVIDAD","DOUBLE","","","","")
arcpy.AddField_management(verificacion,"FECHA","DATE","","","","")
arcpy.AddField_management(verificacion,"APROBACION_SUPERVISOR","TEXT","","","2","")
arcpy.AddField_management(verificacion,"ESTADO","TEXT","","","10","")
arcpy.AddField_management(verificacion,"OBSERVACIONES","TEXT","","","255","")

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
    elif tabla == "Dom_Actividades_Pagos_VR":
        arcpy.AssignDomainToField_management(verificacion,"ACTIVIDAD",tabla)

    elif tabla == "Dom_Contratistas_Control":
        arcpy.AssignDomainToField_management(Control_Calidad,"CONTRATISTA",tabla)
    elif tabla == "Dom_Contratistas_Control_Restitucion":
        arcpy.AssignDomainToField_management(Control_Captura,"CONTRATISTA",tabla)
    elif tabla == "Dom_Contratistas_Edicion":
        arcpy.AssignDomainToField_management(Edicion,"CONTRATISTA",tabla)
    elif tabla == "Dom_Contratistas_Mantenimiento":
        arcpy.AssignDomainToField_management(Mantenimiento_Bases,"CONTRATISTA",tabla)
    elif tabla == "Dom_Contratistas_Verificacion":
        arcpy.AssignDomainToField_management(verificacion,"CONTRATISTA",tabla)

    elif tabla == "Dom_Escala_Pagos":
        arcpy.AssignDomainToField_management(Control_Calidad,"ESCALA",tabla)
        arcpy.AssignDomainToField_management(Edicion,"ESCALA",tabla)
        arcpy.AssignDomainToField_management(Control_Captura,"ESCALA",tabla)
        arcpy.AssignDomainToField_management(Mantenimiento_Bases,"ESCALA",tabla)
        arcpy.AssignDomainToField_management(verificacion,"ESCALA",tabla)
    elif tabla == "Dom_Unidad_Medicion":
        arcpy.AssignDomainToField_management(Control_Calidad,"UNIDAD_MEDICION",tabla)
        arcpy.AssignDomainToField_management(Edicion,"UNIDAD_MEDICION",tabla)
        arcpy.AssignDomainToField_management(Control_Captura,"UNIDAD_MEDICION",tabla)
        arcpy.AssignDomainToField_management(Mantenimiento_Bases,"UNIDAD_MEDICION",tabla)
        arcpy.AssignDomainToField_management(verificacion,"UNIDAD_MEDICION",tabla)
    elif tabla == "Dom_Proyecto_2016":
        arcpy.AssignDomainToField_management(Control_Calidad,"PROYECTO",tabla)
        arcpy.AssignDomainToField_management(Edicion,"PROYECTO",tabla)
        arcpy.AssignDomainToField_management(Control_Captura,"PROYECTO",tabla)
        arcpy.AssignDomainToField_management(Mantenimiento_Bases,"PROYECTO",tabla)
        arcpy.AssignDomainToField_management(verificacion,"PROYECTO",tabla)
    elif tabla == "Dom_Estado_Pagos":
        arcpy.AssignDomainToField_management(Control_Calidad,"ESTADO",tabla)
        arcpy.AssignDomainToField_management(Edicion,"ESTADO",tabla)
        arcpy.AssignDomainToField_management(Control_Captura,"ESTADO",tabla)
        arcpy.AssignDomainToField_management(Mantenimiento_Bases,"ESTADO",tabla)
        arcpy.AssignDomainToField_management(verificacion,"ESTADO",tabla)
    elif tabla == "Dom_Aprobacion_Supervisor":
        arcpy.AssignDomainToField_management(Control_Calidad,"APROBACION_SUPERVISOR",tabla)
        arcpy.AssignDomainToField_management(Edicion,"APROBACION_SUPERVISOR",tabla)
        arcpy.AssignDomainToField_management(Control_Captura,"APROBACION_SUPERVISOR",tabla)
        arcpy.AssignDomainToField_management(Mantenimiento_Bases,"APROBACION_SUPERVISOR",tabla)
        arcpy.AssignDomainToField_management(verificacion,"APROBACION_SUPERVISOR",tabla)



