__author__ = 'fgonzalezf'
import datetime, arcpy,sys

FeatureLayer=sys.argv[1]
CampoFecha= sys.argv[2]

formato = "%m-%d-%Y %I:%M:%S"

Hoy =datetime.datetime.now()
haceTreintaDias = Hoy-datetime.timedelta(days=30)
arcpy.SelectLayerByAttribute_management(FeatureLayer,"NEW_SELECTION","["+CampoFecha+"] > "+"#"+haceTreintaDias.strftime(formato)+"#")
arcpy.AddMessage(haceTreintaDias.strftime(formato))
