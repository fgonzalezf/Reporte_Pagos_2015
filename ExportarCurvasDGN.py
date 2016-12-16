import arcpy, os, sys

DGN=r"X:\PRUEBAS\PACHO\Curvas\BOYACA_10000_BOG_169IVC3_Aprobado.dgn"

arcpy.env.workspace=DGN
ListaFeat= arcpy.ListFeatureClasses()

for fc in ListaFeat:
    desc=arcpy.Describe(fc)
    if desc.shapeType=="Polyline":
        print fc
        expression=""""Level" = 42"""
        expression1=""""Level" = 43"""
        expression2=""""Level" = 44"""
        expression3=""""Level" = 45"""
        CIND=os.path.dirname(DGN)+os.sep+"Curvas_Indices_"+os.path.basename(DGN).split(".")[0]+".shp"
        CINT=os.path.dirname(DGN)+os.sep+"Curvas_Intermedias_"+os.path.basename(DGN).split(".")[0]+".shp"
        CINDD=os.path.dirname(DGN)+os.sep+"Curvas_Indices_depresion_"+os.path.basename(DGN).split(".")[0]+".shp"
        CINTD=os.path.dirname(DGN)+os.sep+"Curvas_Intermedias_depresion_"+os.path.basename(DGN).split(".")[0]+".shp"
        arcpy.FeatureClassToFeatureClass_conversion(fc,os.path.dirname(DGN), os.path.basename(CIND) , expression)
        arcpy.FeatureClassToFeatureClass_conversion(fc,os.path.dirname(DGN), os.path.basename(CINT) , expression1)
        arcpy.FeatureClassToFeatureClass_conversion(fc,os.path.dirname(DGN), os.path.basename(CINDD) , expression2)
        arcpy.FeatureClassToFeatureClass_conversion(fc,os.path.dirname(DGN), os.path.basename(CINTD) , expression3)
        result = int(arcpy.GetCount_management(CIND).getOutput(0))
        result2 = int(arcpy.GetCount_management(CINT).getOutput(0))
        result3 = int(arcpy.GetCount_management(CINDD).getOutput(0))
        result4 = int(arcpy.GetCount_management(CINTD).getOutput(0))
        print CIND
        print CINT
        print CINDD
        print CINTD
        if result==0:
            arcpy.Delete_management(CIND)
        if result2==0:
            arcpy.Delete_management(CINT)
        if result3==0:
            arcpy.Delete_management(CINDD)
        if result4==0:
            arcpy.Delete_management(CINTD)
            





