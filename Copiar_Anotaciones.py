import arcpy,os,sys

Geodatabase = r"X:\PRUEBAS\Departamentales\Modelo_Departamentales\ModeloDepartamentales.gdb"

arcpy.env.workspace=Geodatabase

ListaDatasets=arcpy.ListDatasets()

for dataset in ListaDatasets:
    arcpy.env.workspace=Geodatabase+os.sep+dataset
    ListaFeatureClass= arcpy.ListFeatureClasses()
    for fc in ListaFeatureClass:
        Describe = arcpy.Describe(fc)
        if Describe.featureType=="Annotation":
            if fc.find("_250K")!=-1:
                print fc
                arcpy.Copy_management(fc,Geodatabase+os.sep+dataset+os.sep+fc.replace("250K","150K"))
                arcpy.Copy_management(fc,Geodatabase+os.sep+dataset+os.sep+fc.replace("250K","200K"))
                arcpy.Copy_management(fc,Geodatabase+os.sep+dataset+os.sep+fc.replace("250K","300K"))
                arcpy.Copy_management(fc,Geodatabase+os.sep+dataset+os.sep+fc.replace("250K","400K"))
                arcpy.Copy_management(fc,Geodatabase+os.sep+dataset+os.sep+fc.replace("250K","500K"))
                arcpy.Copy_management(fc,Geodatabase+os.sep+dataset+os.sep+fc.replace("250K","750K"))
                arcpy.Delete_management(fc)
