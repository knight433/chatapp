# from databaseCon import init, userData, Messages, Groups
from autoComplete import NextWord

# init()
# userObj = userData()
# msgObj = Messages()
# grpObj = Groups()
word = NextWord()

# print(userObj.getusers())
# print(grpObj.getGroup('testUser3'))

# msgObj.message('testUser3','groupID4',"this is a test message 2")
# msgObj.loadallmessages()

# print(msgObj.loadGroupMessages('testUser2','groupID4'))

# mes = [{'user': 'testUser3', 'content': 'Overall, it was a wonderful experience.'}]
# text = mes[0]['content']
# print(text) # debugging

next_word_predictor = NextWord()
a = next_word_predictor.nextWords("i was walking")
print(a) 