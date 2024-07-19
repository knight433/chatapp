from databaseCon import init, userData, Messages, Groups

init()
userObj = userData()
msgObj = Messages()
grpObj = Groups()

# print(userObj.getusers())
# print(grpObj.getGroup('testUser3'))

msgObj.message('testUser3','groupID4',"this is a test message 2")
msgObj.loadallmessages()

# print(msgObj.loadGroupMessages('testUser2','groupID4'))

# mes = [{'user': 'testUser3', 'content': 'Overall, it was a wonderful experience.'}]
# text = mes[0]['content']
# print(text) # debugging