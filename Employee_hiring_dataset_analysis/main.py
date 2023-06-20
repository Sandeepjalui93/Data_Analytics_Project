import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import mysql.connector as connection

HOST = 'localhost'
USERNAME = 'root'
PASSWORD = ''
DATABASE = 'hiring_data'

def connect_database():
    mydb = connection.connect(host=HOST, port="3306", database=DATABASE, user=USERNAME, passwd=PASSWORD)
    return mydb

def load_records():
    mydb = connect_database()
    cursor = mydb.cursor()
    selectquery = 'SELECT table_name FROM information_schema.tables WHERE table_type="BASE TABLE" AND table_schema="hiring_data"'
    cursor.execute(selectquery)
    records = cursor.fetchall()
    return records

def arrfilled_arrnonfilled():
    mydb = connect_database()
    cursor = mydb.cursor()

    arrFilledjobs = list()
    arrNonfilledjobs = list()
    arrMonthname = list()
    
    for row in load_records():
        id = row[0]
        filledJobsratio = 0
        nonfilledJobsratio = 0
        nonfilledJobs = 0
        print(str(row))
        
        row1 = str(row)
        row2 = row1.replace("('", " ")
        row2 = row2.replace("',)", " ")
        month_name = str(row2)
        first_three_letters_month = month_name[:4]
        arrMonthname.append(first_three_letters_month)
        selectquery = 'select * from %s'
        
        cursor.execute('select count(*) from %s where `FILLED` !="" ' % month_name)
        
        filledcount = cursor.fetchone()
        cursor.execute('select count(*) from %s where `FILLED` ="" ' % month_name)
        nonfilledcount = cursor.fetchone()
        
        filledcount1 = str(filledcount)
        filledcount2 = filledcount1.replace("(", " ")
        filledcount = filledcount2.replace(",)", " ")
        
        nonfilledcount1 = str(nonfilledcount)
        nonfilledcount2 = nonfilledcount1.replace("(", " ")
        nonfilledcount = nonfilledcount2.replace(",)", " ")
        
        filledJobsratio = (int(filledcount)/(int(filledcount)+int(nonfilledcount)))*100
        nonfilledJobsratio = (int(nonfilledcount)/(int(filledcount)+int(nonfilledcount)))*100
        arrFilledjobs.append(round(filledJobsratio,1))
        arrNonfilledjobs.append(round(nonfilledJobsratio,1))
    
    return arrFilledjobs, arrNonfilledjobs, arrMonthname

arrFilledjobs, arrNonfilledjobs, arrMonthname = arrfilled_arrnonfilled()
print(arrFilledjobs)
print(arrNonfilledjobs)
print(arrMonthname)

x = np.arange(len(arrMonthname))
width = 0.35

fig, ax = plt.subplots()

rects1 = ax.bar(x - width/2, arrFilledjobs, width, label='Filled')
rects2 = ax.bar(x + width/2, arrNonfilledjobs, width, label='Non')

con = ax.containers

ax.set_xlabel('Months')
ax.set_ylabel('Scores')
ax.set_title('Scores of Filled and Non-filled jobs')
ax.set_xticks(x, arrMonthname)
ax.legend()

ax.bar_label(rects1, padding=4)
ax.bar_label(rects2, padding=4)

fig.tight_layout()
plt.show()