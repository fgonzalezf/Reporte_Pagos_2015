import arcpy

admin_workspace = r"D:\Proyecto\backup-conexiones-Arcgis\172.17.2.247@sde.sde"
arcpy.env.workspace = admin_workspace
user_name = "PAGOS"
# Look through the users in the connected user list and get the SDE ID.
# Use the SDE ID to disconnect the user that matches the username variable
users = arcpy.ListUsers(admin_workspace) # The environment is set, no workspace is needed.
for item in users:
    if item.Name == user_name:
        print item.ID
        arcpy.DisconnectUser(admin_workspace, item.ID)
