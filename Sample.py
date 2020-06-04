import os
import pyodbc as db
import sqlparse
import json
import re

codePath = r"Path to Area in Project"
server = "server connection string"
dataBase = "database Name"
userId = "userid"
pwd = "*****"
dbc = 'DRIVER={ODBC Driver 13 for SQL Server};SERVER=' + server +';DATABASE=' + dataBase + ';UID=' + userId + ';PWD=' + pwd
con = db.connect(dbc)
cur = con.cursor()
jsondata = []

try:
    dbc = 'DRIVER={ODBC Driver 13 for SQL Server};SERVER=' + server +';DATABASE=' + dataBase + ';UID=' + userId + ';PWD=' + pwd
    con = db.connect(dbc)
    cur = con.cursor()
    spquery = "SELECT ROUTINE_NAME, ROUTINE_DEFINITION FROM {0}.information_schema.routines".format(dataBase)
    sp_names = cur.execute(spquery).fetchall()
finally:
    cur.close()
details = []
with open("Code_Impact.csv", "w") as csvFile:
    csvFile.write("FileName, SPName\n")
    for root, dirs, files in os.walk(codePath):
        for fileName in files:
            contSpList = []
            if fileName.endswith('Controller.cs'):
                with open(root + '\\' + fileName) as file:
                    filedata = file.readlines()
                for line in filedata:
                    if '//' not in line:
                        for sp in sp_names:
                            if '"' + sp[0] + '"' in line:
                                contSpList.append(sp[0])
                                csvFile.write(str(fileName) + ", " + str(sp[0]) + "\n")
