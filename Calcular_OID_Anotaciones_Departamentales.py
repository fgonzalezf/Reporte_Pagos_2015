import arcpy,os,sys

Geodatabase = r"X:\PRUEBAS\Departamentales\Modelo_Departamentales\BK_Final\Temp2.gdb"

arcpy.env.workspace = Geodatabase

ListaDatasets= arcpy.ListDatasets()

def BuscarCampoTempID(Feat):
    estado = False
    ListaFields= arcpy.ListFields(Feat)
    for field in ListaFields:
        if field.name=="TEMPID":
            estado=True
    return estado

def calcularCampo(FeatAnot,Feat):

    edit = arcpy.da.Editor(Geodatabase)
    edit.startEditing(False, True)
    edit.startOperation()

    arcpy.Delete_management("Layer1")
    arcpy.MakeFeatureLayer_management(FeatAnot,"Layer1")
    arcpy.AddJoin_management("Layer1","FeatureId",Feat,"OBJECTID","KEEP_COMMON")
    print os.path.basename(FeatAnot)+"."+"FeatureId"
    print "["+os.path.basename(Feat)+"."+"TEMPID"+"]"
    arcpy.CalculateField_management("Layer1",os.path.basename(FeatAnot)+"."+"FeatureID","["+os.path.basename(Feat)+"."+"TEMPID"+"]","VB")
    arcpy.Delete_management("Layer1")

    edit.stopOperation()
    edit.stopEditing(True)


for dataset in ListaDatasets:
    arcpy.env.workspace=Geodatabase+ os.sep+dataset
    ListaFc= arcpy.ListFeatureClasses()
    for fc in ListaFc:
        Describe = arcpy.Describe(fc)
        if Describe.featureType=="Simple":
            if BuscarCampoTempID(fc):
                print fc
                try:
                    Feat=Geodatabase+os.sep+dataset+os.sep+fc
                    Anotacion1= Geodatabase+os.sep+dataset+os.sep+fc+"_Anot_150K"
                    Anotacion2= Geodatabase+os.sep+dataset+os.sep+fc+"_Anot_200K"
                    Anotacion3= Geodatabase+os.sep+dataset+os.sep+fc+"_Anot_300K"
                    Anotacion4= Geodatabase+os.sep+dataset+os.sep+fc+"_Anot_350K"
                    Anotacion5= Geodatabase+os.sep+dataset+os.sep+fc+"_Anot_400K"
                    Anotacion6= Geodatabase+os.sep+dataset+os.sep+fc+"_Anot_500K"
                    Anotacion7= Geodatabase+os.sep+dataset+os.sep+fc+"_Anot_750K"

                    calcularCampo(Anotacion1,Feat)
                    calcularCampo(Anotacion2,Feat)
                    calcularCampo(Anotacion3,Feat)
                    calcularCampo(Anotacion4,Feat)
                    calcularCampo(Anotacion5,Feat)
                    calcularCampo(Anotacion6,Feat)
                    calcularCampo(Anotacion7,Feat)

                except Exception as e:
                    print "error: " + e.message
