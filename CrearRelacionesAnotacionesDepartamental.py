import arcpy, os ,sys

Dataset=sys.argv[1]

arcpy.env.workspace=Dataset

ListaFeatuares= arcpy.ListFeatureClasses("*","Annotation")
if arcpy.TestSchemaLock(Dataset):
    for fcAnot in ListaFeatuares:
        fcOrig= fcAnot.split("_Anot")[0]
        if arcpy.Exists(fcOrig):
            arcpy.AddMessage("Anotacion..."+fcAnot)
            arcpy.AddMessage("Origen...."+fcOrig)
            NombreRel= fcAnot+"_Rel"
            arcpy.AddMessage("Nombre Relacion..."+NombreRel)
            try:
                arcpy.CreateRelationshipClass_management(fcOrig,fcAnot,NombreRel,"COMPOSITE",fcOrig,fcAnot,"FORWARD", "ONE_TO_MANY", "NONE", "OBJECTID","FeatureID")
            except Exception as e:
                arcpy.AddWarning( "Error Creando Relacion: "+e.message)
    del ListaFeatuares
else:
    arcpy.AddWarning("Esquema Bloqueado No se puede Crear Relaciones")
