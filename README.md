# Allscripts-Import
This is a program I developed and deployed and currently have working in production at my organization Starling Physicians. It is used to take image files (jpeg, png etc)
and rename them in a certain filenaming convention and drop them into a network folder where they are picked up by a third party import service and imported into Allscripts
Touchworks EHR, the medical records management system. 

The program works as follows:
The user drops the jpeg files into an Import folder which they have a shortcut to on their Windows desktop. 
The user opens my program which launches the python tkinter GUI
User enters the Patient ID into the gui and clicks submit
My program looks in the import folder, renames each file with a certain filename convention which contains a hardcoded Org ID and Folder ID, inserts the Patient ID into filename
as well, and then moves the files into the network sweep folder.
