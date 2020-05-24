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

def saveRoles(ctx):
    role_list = []
    for role in ctx.guild.get_member(ctx.message.author.id).roles:
        role_list.append(role.id)
    cursor.execute("""INSERT INTO savedroles(id,roles) VALUES('{0}',"{1}") ON DUPLICATE KEY UPDATE roles = "{1}";""".format(ctx.message.author.id,role_list))
    connection.commit()
    return role_list

def getRoles(id):
    cursor.execute("SELECT roles FROM savedroles WHERE id='{0}'".format(id))
    result = cursor.fetchone()[0].decode('utf-8').strip("][").split(', ')
    return result

async def restoreRoles(member):
    role_list = getRoles(member.id)
    for role in role_list[1:]:
        resolved_role = member.guild.get_role(int(role))
        await member.add_roles(resolved_role)