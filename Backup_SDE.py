import arcpy, os,sys

GeodatabaseSDE= r"X:\Conexiones_SDE\propias\fgonzalez_admin.sde"
GeodatabaseSalida= r"X:\PRUEBAS\BackUp Corporativa Control\BK_09_12_2016_.mdb"

arcpy.CreatePersonalGDB_management(os.path.dirname(GeodatabaseSalida),os.path.basename(GeodatabaseSalida))
dataset= GeodatabaseSDE + os.sep + "ADMIN_GIT_PC.PLANCHAS"
try:
    arcpy.AddMessage("Copiando")
    arcpy.Copy_management(dataset,GeodatabaseSalida+os.sep+"PLANCHAS")
except Exception as e:
    arcpy.AddMessage("Error Ejecutando copia"+ e.message)
