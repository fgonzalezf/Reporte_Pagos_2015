import arcpy, os, sys

Geodatabase = sys.argv[1]


def verificarCampo(Feat, nombre):
    existe=True
    ListaFeatures = arcpy.ListFields(Feat)
    for field in ListaFeatures:
        if field.name.upper()==nombre.upper():
            existe=False
    return existe


arcpy.env.workspace = Geodatabase

ListaDatasets= arcpy.ListDatasets("Transporte_Terrestre", "Feature")

for dataset in ListaDatasets:
    arcpy.env.workspace= Geodatabase+ os.sep+ dataset
    ListaFeats = arcpy.ListFeatureClasses("Via")
    for fc in ListaFeats:
        if fc.upper() == "Via".upper() and verificarCampo(fc,"EJE_VIAL"):
            try:
                arcpy.AddField_management(fc,"EJE_VIAL","TEXT","","","100","EJE_VIAL")
                arcpy.AddMessage("Campo Agregado correctamente")
            except:
                arcpy.AddMessage("Esquema Bloqueado Intentelo Nuevamente")
        else:
            arcpy.AddMessage("El Campo Ya Existe")


