import mysql.connector as mysql
import random

connection = mysql.connect(user="dummybot",host="localhost",database="POLE")
cursor = connection.cursor()

def getFact():
    cursor.execute("SELECT * FROM datos")
    result = cursor.fetchall()
    fact = str(result[random.randint(0,len(result) - 1)])[2:-3]
    return fact

def addFact(arg):
    cursor.execute("INSERT INTO datos(dato) VALUES('{0}')".format(arg))
    connection.commit()
    return

def saveRoles(id,roles):
    cursor.execute("""INSERT INTO savedroles(id,roles) VALUES('{0}',"{1}")""".format(id,roles))
    connection.commit()
    return