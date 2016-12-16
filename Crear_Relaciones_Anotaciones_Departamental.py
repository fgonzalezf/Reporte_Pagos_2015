import arcgisscripting, sys, string, os, arcpy
gp = arcgisscripting.create()
Geodatabase= r"X:\Conexiones_SDE\propias\fernandogonzalez_100K.sde"


gp.workspace = Geodatabase
datasets2 = gp.listdatasets("ADMCIENMIL*", "FEATURE")
dataset2 = datasets2.next()

while dataset2:
          gp.workspace = Geodatabase + "\\" + dataset2
          fcs2 = gp.ListFeatureClasses()
          fcs2.reset()
          fc2 = fcs2.next()
          while fc2:
              desc = arcpy.Describe(fc2)
              if desc.featureType =="Annotation":
                 try:

                     if fc2.find("_150K")!=-1:
                         Feat=Geodatabase + "\\" + dataset2+os.sep+fc2.replace("_Anot_150K","")
                     elif fc2.find("_200K")!=-1:
                         Feat=Geodatabase + "\\" + dataset2+os.sep+fc2.replace("_Anot_200K","")
                     elif fc2.find("_300K")!=-1:
                         Feat=Geodatabase + "\\" + dataset2+os.sep+fc2.replace("_Anot_300K","")
                     elif fc2.find("_400K")!=-1:
                         Feat=Geodatabase + "\\" + dataset2+os.sep+fc2.replace("_Anot_400K","")
                     elif fc2.find("_500K")!=-1:
                         Feat=Geodatabase + "\\" + dataset2+os.sep+fc2.replace("_Anot_500K","")
                     elif fc2.find("_750K")!=-1:
                         Feat=Geodatabase + "\\" + dataset2+os.sep+fc2.replace("_Anot_750K","")
                     elif fc2.find("_500K")!=-1:
                         Feat=Geodatabase + "\\" + dataset2+os.sep+fc2.replace("_Anot_500K","")
                     else:
                         Feat=Geodatabase + "\\" + dataset2+os.sep+fc2.replace("_Anot","")
                     print "Entrada: " + Feat
                     print "Salida: " + fc2
                     print "Nombre Relacion: "+Geodatabase + "\\" + dataset2+ os.sep+ fc2+"_Rel"
                     print "Nombre Etiqueta: " + fc2.replace("_Anot","").replace("_150K","").replace("_200K","").replace("_300K","").replace("_400K","").replace("_500K","").replace("_750K","")

                     gp.CreateRelationshipClass_management(Feat, fc2, Geodatabase + "\\" + dataset2+ os.sep+ fc2+"_Rel" , "COMPOSITE", fc2, fc2.replace("_Anot","").replace("_150K","").replace("_200K","").replace("_300K","").replace("_400K","").replace("_500K","").replace("_750K","") , "FORWARD", "ONE_TO_MANY", "NONE", "OBJECTID", "FeatureID", "", "")
                     gp.AddMessage("Relacion Creada:" + Geodatabase + "\\" + dataset2+ os.sep+ fc2+"_Rel")
                 except:
                     gp.AddMessage("Relacion ya Existente:" + Geodatabase + "\\" + dataset2+ os.sep+ fc2+"_Rel")
              fc2 = fcs2.next()
          dataset2 = datasets2.next()


