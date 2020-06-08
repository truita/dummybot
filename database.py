import mysql.connector as mysql
import random
import os

def getconnection(): #This function is called whenever it is needed to get a connection to the db
    connection = mysql.connect(user="dummybot",host="localhost",database="POLE") #Connects
    return connection,connection.cursor(buffered=True) #Returns the connection along with its cursor

def closeconnection(connection,cursor): #This function is called to close a connection properly
    connection.close()
    cursor.close()

def getFact(): #Used to get a random fact from the db
    connection,cursor = getconnection()
    cursor.execute("SELECT * FROM datos") #Queries all the facts
    result = cursor.fetchall() #Saves the facts to a variable
    random.seed(os.urandom(50))
    fact = str(result[random.randint(0,len(result) - 1)])[2:-3] #Chooses a fact randomly
    closeconnection(connection,cursor)
    return fact #Returns the fact

def addFact(arg): #Used to save a fact in the db
    connection,cursor = getconnection()
    cursor.execute("INSERT INTO datos(dato) VALUES('{0}')".format(arg)) #Adds the fact
    connection.commit() #Commits changes
    closeconnection(connection,cursor)
    return

def saveRoles(ctx): #Used to save the roles of a member before kicking him
    connection,cursor = getconnection()
    role_list = [] #Defines role_list as an array
    for role in ctx.guild.get_member(ctx.message.author.id).roles: #Adds the roles of the user to role_list
        role_list.append(role.id)
    cursor.execute("""INSERT INTO savedroles(id,roles) VALUES('{0}',"{1}") ON DUPLICATE KEY UPDATE roles = "{1}";""".format(ctx.message.author.id,role_list)) #Adds the array into the database
    connection.commit() #Commits changes
    closeconnection(connection,cursor)
    return

def getRoles(id):
    connection,cursor = getconnection()
    cursor.execute("SELECT roles FROM savedroles WHERE id='{0}'".format(id)) #Gets the roles from db
    result = cursor.fetchone()[0].decode('utf-8').strip("][").split(', ') #Transform the array representation into an actual array
    closeconnection(connection,cursor)
    return result #Returns the array

async def restoreRoles(member):
    connection,cursor = getconnection()
    role_list = getRoles(member.id) #Gets the list of roles
    for role in role_list[1:]: #Removes the first role in the array because it always is @everyone
        resolved_role = member.guild.get_role(int(role)) #Transform the role id into a Role object
        await member.add_roles(resolved_role) #Adds the role to the user
    closeconnection(connection,cursor)

def savePole(id):
    connection,cursor = getconnection()
    cursor.execute("INSERT INTO scores(id,points,pole) VALUES({0},4,1) ON DUPLICATE KEY UPDATE points = points + 4, pole = pole + 1".format(id)) #Adds the user and its points, if it already exists it will update its points
    connection.commit() #Commits changes
    closeconnection(connection,cursor)
    return

def saveSubpole(id): #Very similar to savePole
    connection,cursor = getconnection()
    cursor.execute("INSERT INTO scores(id,points,subpole) VALUES({0},2,1) ON DUPLICATE KEY UPDATE points = points + 2, subpole = subpole + 1".format(id))
    connection.commit()
    closeconnection(connection,cursor)
    return

def saveFail(id): #Very similar to savePole
    connection,cursor = getconnection()
    cursor.execute("INSERT INTO scores(id,points,fail) VALUES({0},1,1) ON DUPLICATE KEY UPDATE points = points + 1, fail = fail + 1".format(id))
    connection.commit()
    closeconnection(connection,cursor)
    return

def getRanking():
    connection,cursor = getconnection()
    ranking_matrix = [[[0 for x in range(2)] for y in range(3)] for z in range(4)] #Defines a tridimensional array for the points/users to be stored
    cursor.execute("SELECT id,points FROM scores ORDER BY points DESC LIMIT 3;") #Gets the users and its global points
    ranking_matrix[0] = cursor.fetchall() #Saves them to the first slot of the variable
    cursor.execute("SELECT id,pole FROM scores ORDER BY pole DESC LIMIT 3;") #Gets the users and its number of poles made
    ranking_matrix[1] = cursor.fetchall() #Saves them to the second slot of the variable
    cursor.execute("SELECT id,subpole FROM scores ORDER BY subpole DESC LIMIT 3;")#Gets the users and its number of subpoles made
    ranking_matrix[2] = cursor.fetchall() #Saves them to the third slot of the variable
    cursor.execute("SELECT id,fail FROM scores ORDER BY fail DESC LIMIT 3;")#Gets the users and its number of fails made
    ranking_matrix[3] = cursor.fetchall() #Saves them to the fourth slot of the variable
    closeconnection(connection,cursor)
    return ranking_matrix