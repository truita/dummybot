import mysql.connector as mysql
import random

connection = mysql.connect(user="dummybot",host="localhost",database="POLE")
cursor = connection.cursor()

cursor.execute("SELECT * FROM datos")
result = cursor.fetchall()
print(result[random.randint(0,len(result))])

def getFacts():
    cursor.execute("SELECT * FROM datos")
    result = cursor.fetchall()
    return result[random.randint(0,len(result))]