import pymysql
import pandas as pd
from flask import Flask , session
def convert_listItems_int(list):
    res = [eval(str(i)) for i in list]
    return res

def connect_database_server():
    try:
        connection = pymysql.connect(host="localhost", user="root", passwd="")
        db = connection.cursor()
        return db,connection
    except:
        print("\033[91mFAILED TO CONNECT WITH YOUR DATABASE\033[0m")
        exit()

def connect_database(dbName):
    try:
        connection = pymysql.connect(host="localhost", user="root", passwd="", database=f"{dbName}")
        db = connection.cursor()
        return db,connection
    except:
        print("\033[91mFAILED TO CONNECT WITH YOUR DATABASE\033[0m")
        exit()

def pieChart(db,sem):
    db.execute(f"SELECT COUNT(DISTINCT(`NAME OF STUDENT`)) FROM {session['tableN']} WHERE SEM={sem} AND `SUBJECT CODE`=121 OR `SUBJECT CODE`=111")
    result = db.fetchall()
    total_student=result[0][0]
    db.execute(f"SELECT COUNT(DISTINCT(`NAME OF STUDENT`)) FROM {session['tableN']} WHERE SEM={sem} AND `SEM {sem}`!='F' AND `GENDER`=' M'")
    result = db.fetchall()
    passedBoys = int(result[0][0])
    db.execute(f"SELECT COUNT(DISTINCT(`NAME OF STUDENT`)) FROM {session['tableN']} WHERE SEM={sem} AND `SEM {sem}`!='F' AND `GENDER`=' F'")
    result = db.fetchall()
    passedGirls = int(result[0][0])
    db.execute(f"SELECT COUNT(DISTINCT(`NAME OF STUDENT`)) FROM {session['tableN']} WHERE SEM={sem} AND `SEM {sem}`='F' AND `GENDER`=' M'")
    result = db.fetchall()
    failedBoys = int(result[0][0])
    db.execute(f"SELECT COUNT(DISTINCT(`NAME OF STUDENT`)) FROM {session['tableN']} WHERE SEM={sem} AND `SEM {sem}`='F' AND `GENDER`=' F'")
    result = db.fetchall()
    failedGirls = int(result[0][0])
    res=[passedBoys,passedGirls,failedBoys,failedGirls]
    return res

def get_subjectList(db,sem):
    db.execute(f"SELECT DISTINCT(`SUBJECT CODE`) FROM {session['tableN']} WHERE SEM={sem}")
    result = db.fetchall()
    subjectList = []
    for each in result:
        subjectList.append(each[0])
    return subjectList

def get_subject_analysis(db,sem,table_name):
    subjectList=get_subjectList(db,sem)
    if "423" in subjectList:
        subjectList.remove("423")
    avgMarksbarChartDict = {}
    minMarksbarChartDict = {}
    maxMarksbarChartDict = {}
    failedChartDict = {}

    analysis_data=[]

    for i in range(len(subjectList)):
        db.execute(f"SELECT MAX(`EXTERNAL`) FROM {table_name} WHERE SEM={sem} AND `SUBJECT CODE`='{subjectList[i]}' AND `EXTERNAL`!=0 AND `EXTERNAL`!=' AA'")
        result = db.fetchall()

        if result[0][0] != 0.0 and result[0][0] != None:
            maxMarksbarChartDict[f"{subjectList[i]}"] = int(result[0][0])
            max_m = int(result[0][0])

            db.execute(
                f"SELECT MIN(`EXTERNAL`) FROM {table_name} WHERE SEM={sem} AND `SUBJECT CODE`='{subjectList[i]}' AND `EXTERNAL`!=0 AND `EXTERNAL`!=' AA'")
            result = db.fetchall()
            minMarksbarChartDict[f"'{subjectList[i]}'"] = int(result[0][0])
            min_m = int(result[0][0])

            db.execute(
                f"SELECT AVG(`EXTERNAL`) FROM {table_name} WHERE SEM={sem} AND `SUBJECT CODE`='{subjectList[i]}'")
            result = db.fetchall()
            avgMarksbarChartDict[f"'{subjectList[i]}'"] = round(result[0][0], 2)
            avg_m = round(result[0][0], 2)

            db.execute(
                f"SELECT COUNT(DISTINCT(`NAME OF STUDENT`)) FROM {table_name} WHERE SEM={sem} AND `SUBJECT CODE`='{subjectList[i]}' AND `GRADE POINT`!='FF'")
            result = db.fetchall()
            passed_stud = int(result[0][0])

            db.execute(
                f"SELECT COUNT(DISTINCT(`NAME OF STUDENT`)) FROM {table_name} WHERE SEM={sem} AND `SUBJECT CODE`='{subjectList[i]}' AND `GRADE POINT`='FF'")
            result = db.fetchall()
            failedChartDict[f"'{subjectList[i]}'"] = int(result[0][0])
            fail_stud = int(result[0][0])

            db.execute(
                f"SELECT COUNT(DISTINCT(`NAME OF STUDENT`)) FROM {table_name} WHERE SEM={sem} AND `SUBJECT CODE`='{subjectList[i]}' AND `GRADE POINT`!='FF' AND `EXTERNAL` < {avg_m}")
            result = db.fetchall()
            below_avg = int(result[0][0])

            tmp_list = [subjectList[i], min_m, avg_m, max_m, passed_stud, fail_stud, below_avg]
            analysis_data.append(tmp_list)

    df_analysis = pd.DataFrame(analysis_data,
                               columns=['Subject', 'Min', 'Avg', 'Max', 'Passed', 'Failed', 'Below Average'])


    return df_analysis['Subject'].values.tolist(), df_analysis['Min'].values.tolist(), df_analysis['Avg'].values.tolist(), df_analysis['Max'].values.tolist(), df_analysis['Failed'].values.tolist(),df_analysis['Below Average'].values.tolist()

def get_sem_list(db,table_name):
    semList = []
    tb_n=table_name
    db.execute(f"SELECT DISTINCT(`SEM`) FROM `{tb_n}`")
    result = db.fetchall()
    for each in result:
        semList.append(each[0])
    return semList

def get_table_name(db,db_name):
    db.execute(f"SHOW TABLES FROM `{db_name}`")
    result = db.fetchall()
    res = result[0][0]
    print(res)
    return res