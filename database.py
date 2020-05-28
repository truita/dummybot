import mysql.connector as mysql
import random

connection = mysql.connect(user="dummybot",host="localhost",database="POLE")

def getFact():
    cursor = connection.cursor(buffered=True)
    cursor.execute("SELECT * FROM datos")
    result = cursor.fetchall()
    fact = str(result[random.randint(0,len(result) - 1)])[2:-3]
    cursor.close()
    return fact

def addFact(arg):
    cursor = connection.cursor(buffered=True)
    cursor.execute("INSERT INTO datos(dato) VALUES('{0}')".format(arg))
    connection.commit()
    cursor.close()
    return

def saveRoles(ctx):
    cursor = connection.cursor(buffered=True)
    role_list = []
    for role in ctx.guild.get_member(ctx.message.author.id).roles:
        role_list.append(role.id)
    cursor.execute("""INSERT INTO savedroles(id,roles) VALUES('{0}',"{1}") ON DUPLICATE KEY UPDATE roles = "{1}";""".format(ctx.message.author.id,role_list))
    connection.commit()
    cursor.close()
    return role_list

def getRoles(id):
    cursor = connection.cursor(buffered=True)
    cursor.execute("SELECT roles FROM savedroles WHERE id='{0}'".format(id))
    result = cursor.fetchone()[0].decode('utf-8').strip("][").split(', ')
    cursor.close()
    return result

async def restoreRoles(member):
    cursor = connection.cursor(buffered=True)
    role_list = getRoles(member.id)
    for role in role_list[1:]:
        resolved_role = member.guild.get_role(int(role))
        await member.add_roles(resolved_role)
    cursor.close()

def savePole(id):
    cursor = connection.cursor(buffered=True)
    cursor.execute("INSERT INTO scores(id,points,pole) VALUES({0},4,1) ON DUPLICATE KEY UPDATE points = points + 4, pole = pole + 1".format(id))
    connection.commit()
    cursor.close()
    return

def saveSubpole(id):
    cursor = connection.cursor(buffered=True)
    cursor.execute("INSERT INTO scores(id,points,subpole) VALUES({0},2,1) ON DUPLICATE KEY UPDATE points = points + 2, subpole = subpole + 1".format(id))
    connection.commit()
    cursor.close()
    return

def saveFail(id):
    cursor = connection.cursor(buffered=True)
    cursor.execute("INSERT INTO scores(id,points,fail) VALUES({0},1,1) ON DUPLICATE KEY UPDATE points = points + 4, fail = fail + 1".format(id))
    connection.commit()
    cursor.close()
    return

def getRanking():
    cursor = connection.cursor(buffered=True)
    ranking_matrix = [[[0 for x in range(2)] for y in range(3)] for z in range(4)]
    cursor.execute("SELECT id,points FROM scores ORDER BY points DESC LIMIT 3;")
    ranking_matrix[0] = cursor.fetchall()
    cursor.execute("SELECT id,pole FROM scores ORDER BY pole DESC LIMIT 3;")
    ranking_matrix[1] = cursor.fetchall()
    cursor.execute("SELECT id,subpole FROM scores ORDER BY subpole DESC LIMIT 3;")
    ranking_matrix[2] = cursor.fetchall()
    cursor.execute("SELECT id,fail FROM scores ORDER BY fail DESC LIMIT 3;")
    ranking_matrix[3] = cursor.fetchall()
    cursor.close()
    return ranking_matrix