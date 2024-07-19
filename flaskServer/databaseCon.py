from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import re

class init:
    def __init__(self):
        global users
        global messages
        global groups
        global userobj

        client = MongoClient("mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000")
        db = client.neutaldb
        users = db.users
        messages = db.msg 
        groups = db.groups

        userobj = userData()



class userData:
    
    def __init__(self):
        # Template for user data
        self.userTemplate = {
            "_id" : "",
            "username" : "",
            "password" : ""
        }

    def addUser(self, userid, password):
    
        count = users.count_documents({})
        self.userTemplate["username"] = userid
        self.userTemplate['_id'] = f"userID{count + 1}"
        self.userTemplate["password"] = password

        #not added feature where duplicate users can view
        try:
            
            users.insert_one(self.userTemplate)
            print("User added successfully!")
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def loginAuth(self, userid, password):

        query = {"username": userid}
        
        try:
            user = users.find_one(query)
            
            if user is None:
                print("No user found with that username.")
                st = "No user found with that username."
                return [False,st]
            
            if user["password"] == password:
                print("Login successful!")
                return [True,"Login successful!"]
            else:
                print("Incorrect password.")
                return [False,"Incorrect password."]
        
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
        
    def getusers(self):
        
        u = users.find()
        print(list(u)) 

    def UsernameToid(self, id):
        name = users.find_one({'username': id})
        return name['_id']
    
    def idToUsername(self, id):
        name = users.find_one({'_id': id})
        return name['username']

class Groups:
    
    def __init__(self):
        self.template = {
            "_id": "",  
            "name": "",    
            "members": [], 
            "admin": "",
        }

    def newGroup(self, groupeName: str, listOfmembers):
        
        self.template["name"] = groupeName
        self.template["members"] = list(listOfmembers)  # must make sure there are no unknown users in front end
        count = groups.count_documents({})
        self.template["admin"] = str(listOfmembers[0])
        self.template["_id"] = f"groupID{count + 1}"

        try:
            groups.insert_one(self.template)
            print("Group added successfully!")
        except Exception as e:
            print(f"An error occurred: {e}")

    def getGroup(self, username='all', giveid=True):
        
        if username == 'all':
            g = groups.find()
            return list(g)
        else:
            query = {"members": username}
            g = groups.find(query)
            
            if giveid == True:
                idlist = [id['_id'] for id in g]
                return list(idlist)
            
            return list(g)

class Messages:

    def __init__(self):

        self.msgTemplate = {
            "_id": "",       
            "sender_username": "",
            "sender_id":"",
            "groupID": "",
            "content": ""
        }


    @staticmethod
    def extract_int_from_id(doc):
        match = re.search(r'\d+$', doc['_id'])
        return int(match.group()) if match else float('inf')

    def message(self, userFrom, groupID, message):
        
        count = messages.count_documents({})
        self.msgTemplate['_id'] = f"msg{groupID}{count + 1}"
        self.msgTemplate['sender_username'] = userFrom
        self.msgTemplate['groupID'] = groupID
        self.msgTemplate['content'] = message

        id = userobj.UsernameToid(userFrom)
        self.msgTemplate['sender_id'] = id

        try:
            messages.insert_one(self.msgTemplate)
            print("Message sent successfully!")
        except Exception as e:
            print(f"An error occurred: {e}")
    
    def loadallmessages(self):
        print(list(messages.find()))

    def loadGroupMessages(self, username, groupID):
        
        query = {'groupID': groupID}

        mesg = list(messages.find(query))
        # print(mesg)
        sorted_mesg = sorted(mesg, key=self.extract_int_from_id)
        listOfMessages = []

        for msg in sorted_mesg:
            userName = msg['sender_username']
            content = msg['content']

            temp = {'user': userName,'content': content}
            listOfMessages.append(temp)
        
        return listOfMessages
