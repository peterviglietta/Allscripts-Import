
import os, shutil, sys
import ctypes 
from SETTINGS import setup
from tkinter import *
from tkinter import ttk
import subprocess
import datetime
import sqlite3
from sqlite3 import Error


# Open windows explorer to the Import folder upon launching the app:
subprocess.run('explorer c:\Development\sqlite\\allscripts import\system files\system\import')

# DB functions for audit tables, to be used in Click function
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def insert_imports_row(conn, imports_row):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    sql = ''' INSERT INTO imports(datetime_imported,mrn)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, imports_row)
    conn.commit()
    return cur.lastrowid


def click():
	entered_text=textEntry.get()
	patientid = entered_text
	textEntry.delete(0, END)
	src = r'C:\\development\\sqlite\\Allscripts Import\\System Files\\system\\import\\'

	# Raise an error if the MRN field is blank when Submit is clicked.
	if (entered_text == ''):
		ctypes.windll.user32.MessageBoxW(0, 'Please enter the MRN.', 'Error', 0)
		raise Exception("Please enter the MRN.")
	

	list = os.listdir(src)

	if list == []:
		ctypes.windll.user32.MessageBoxW(0, 'ERROR - There are no files in the import folder.', 'Error', 0)
		raw_input("Pausing due to no files in import folder")
		'''sys.exit()'''

# File size check:
	for i in list:
		if os.stat(src+'\\'+i).st_size > 4999999:
			ctypes.windll.user32.MessageBoxW(0, 'ERROR - File size can not exceed 500KB. Please fix the files and try again.', 'Error', 0)
			sys.exit()

	for counter, value in enumerate(list):
		if value in ['Import.lnk']:
			pass
		elif value.endswith('.pdf'):
			os.rename(src + str(value), src + '72029_' + patientid + "_" + '1316' +'_'+str(counter) +'.pdf')
		elif value.endswith('.jpg'):
			os.rename(src + str(value), src + '72029_' + patientid + "_" + '1316' +'_'+str(counter) +'.jpg')
		elif value.endswith('.png'):
			os.rename(src + str(value), src + '72029_' + patientid + "_" + '1316' +'_'+str(counter) +'.png')
		else:
			ctypes.windll.user32.MessageBoxW(0, 'ERROR - Only jpg, pdf, png files can be imported. No files have been imported. Please fix the files and try again.', 'Error', 0)
			sys.exit()


	renamedList = os.listdir(src)

	for i in renamedList:
		if i in ['Import.lnk']:
			pass
		else:
			shutil.move(src + str(i), r"\\npsprdscan-001.npsmdit.com\ieximports$\Allscripts_Import")


	database = r"C:\development\sqlite\allscripts import\db\falconsqlite.db"

	sql_create_imports_table = """ CREATE TABLE IF NOT EXISTS imports (id integer PRIMARY KEY, datetime_imported text, mrn integer NOT NULL); """

	# create a database connection
	conn = create_connection(database)

    #create tables
	if conn is not None:
		create_table(conn, sql_create_imports_table)
	else: print("Error - Cannot create database connection")

	with conn:
		import_data = (datetime.datetime.now(), patientid)
		insert_imports_row(conn, import_data)
	
	return ctypes.windll.user32.MessageBoxW(0, ('Done. The file(s) have been imported into the chart in Allscripts under Diagnostics > Photos for patient MRN %s.' % patientid), 'Starling EHR Team' , 0)



#######################
####  Tkinter GUI  ####
#######################

# Main Screen:
screen = Tk()
screen.geometry("394x450")
screen.title("Allscripts Photo Import")
screen['bg'] = 'white'

myPhoto = PhotoImage(file="AS Import Logo.png")
Label(screen, image=myPhoto, bg="white").grid(row=0, column=0, sticky=W)
Label(screen, text = "Enter MRN: ", bg="white") .place(x=40, y=150)
textEntry = Entry(screen, width=20, bg="white")
textEntry.place(x=120, y=150)
Button(screen, text="Import", width=6, command=click).place(x=255, y=146)
Label(screen, text = "Step 1:   Make sure all of your files are placed in the Import folder", bg="white") .place(x=10, y=230)
Label(screen, text = "               (There should be nothing else in there except your files)", bg="white") .place(x=10, y=250)
Label(screen, text = "Step 2:   Enter the MRN above and click Import", bg="white") .place(x=10, y=277)
Label(screen, text = "Step 3:   The files will now be in the patient's chart under the", bg="white") .place(x=10, y=308)
Label(screen, text = "Diagnostics > Photos section", bg="white") .place(x=55, y=328)
Label(screen, text = "Use the audit log to check MRNs of previous imports.", bg="white") .place(x=50, y=412)



def openAuditLoad():

	database = r"C:\development\sqlite\allscripts import\db\falconsqlite.db"
	conn = create_connection(database)
	
	auditWindow = Tk()
	wrapper1 = LabelFrame(auditWindow, text = "Audit Entries List")
	sb = Scrollbar(wrapper1)
	sb.pack(side = RIGHT, fill = Y)
	wrapper1.pack(fill="both", expand="yes", padx=20, pady=10)

	trv = ttk.Treeview(wrapper1, columns=(1, 2), show="headings", height="20")
	trv.heading(1, text='Date/Time Imported')
	trv.heading(2, text='Patient MRN')
	trv.pack()

	cur = conn.cursor()
	cur.execute("SELECT datetime_imported, mrn FROM imports ORDER BY datetime_imported desc")
	rows = cur.fetchall()
	print (rows)
	for i in rows:
		trv.insert('', 'end', values=i)

	return rows

auditButton = Button(screen, text="Audit Log", width=11, command=openAuditLoad).place(x=142, y=370)


screen.mainloop()

