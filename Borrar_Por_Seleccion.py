import arcpy, os, sys

Geodatabase = r"D:\Proyecto\EDICION\INTEGRADAS_25K_BORRAR\File_Integrada_2016_v7.gdb"
shape= r"D:\Proyecto\EDICION\INTEGRADAS_25K_BORRAR\Borrar.shp"
arcpy.env.workspace = Geodatabase

Datasets = arcpy.ListDatasets()

for dataset in Datasets:
    arcpy.env.workspace=Geodatabase+os.sep+dataset
    FeaturesClases= arcpy.ListFeatureClasses()
    for fc in FeaturesClases:
        pathFeature=Geodatabase+os.sep+dataset+os.sep+fc
        result = arcpy.GetCount_management(pathFeature)
        count = int(result.getOutput(0))
        if count>0:
            try:
                arcpy.Delete_management("Layer")
            except:
                pass
            layer1=arcpy.MakeFeatureLayer_management(pathFeature,"Layer")
            layer2=arcpy.SelectLayerByLocation_management ("Layer", "INTERSECT",shape,"-5 Meters","NEW_SELECTION")
            result = int(arcpy.GetCount_management("Layer").getOutput(0))
            if result !=0:
                print "Borrando Featuares "+fc+"..."+ str(result)
                arcpy.DeleteFeatures_management("Layer")
            del layer1
            del layer2

