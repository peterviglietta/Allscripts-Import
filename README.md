# Allscripts-Import
This is a program I developed and deployed and currently have working in production at my organization Starling Physicians. It is used to take image files (jpeg, png etc)
and rename them in a certain filenaming convention and drop them into a network folder where they are picked up by a third party import service and imported into Allscripts
Touchworks EHR, the medical records management system. The program also includes a SQLite db where audit information is stored and retreived to the front end.

The program works as follows:
The user drops the jpeg files into an Import folder which they have a shortcut to on their Windows desktop. 
The user opens my program which launches the python tkinter GUI
User enters the Patient ID into the gui and clicks Submit
My program looks in the import folder, renames each file with a certain filename convention which contains a hardcoded Org ID and Folder ID, inserts the Patient ID into filename
as well, and then moves the files into the network sweep folder.
If there are no files in the folder, or if the PatientID field is blank, an error is thrown when the Submit button is clicked.
The patient ID and date time are saved into a SQLITE DB audit table.
If the user needs to go back and check which PatientID they entered, they click the Audit Log button in the GUI and it opens another tkinter window which displays rows from the 
audit tabes in sqlite.

This is a rudimentary program that I hope serves to demonstrate my knowledge of Python and SQL.
