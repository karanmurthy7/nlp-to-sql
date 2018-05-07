from slackclient import SlackClient
import time, sys, html
from database import Database
from parse_user_input import UserInputUtility
import os

class SlackCommunication(object):
    API_KEY = ''
    def __init__(self):
        print(os.getcwd())
        SlackCommunication.API_KEY = sys.argv[1]
        self.slack_client = SlackClient(SlackCommunication.API_KEY)
        self.appName = 'test-bot'
        self.db = Database()
        self.user_input_utility = UserInputUtility()
        
    def slackConnection(self):
        return self.slack_client.rtm_connect()
    
    def slackReadRTM(self):
        return self.slack_client.rtm_read()
    
    
    def parseSlackInput(self, input, botID):
        botAtID = '<@' + botID + '>'
        if input and len(input) > 0:
            input = input[0]
            if 'text' in input and botAtID in input['text']:
                user = input['user']
                message = input['text'][input['text'].index(' '):].strip()
                channel = input['channel']
                return [str(user), str(message), str(channel)]
            else:
                return [None, None, None]
            
    def getBotID(self, botUserName):
        users_list = self.slack_client.api_call('users.list')
        if (users_list):
            users = users_list['members']
            for user in users:
                if ('name' in user and botUserName == user['name'] and not user.get('deleted')):
                    return user.get('id')
                
    def writeToSlack(self, channel, message):
        if message:
            print('input from slack --------------->>>>', message)
            message = html.unescape(message)
            # sql_output = self.db.fetch_data(message)
            sql_output = self.user_input_utility.fetch_response_from_model(self.user_input_utility.model) 
            print('returned output---------> ', sql_output)  
            return self.slack_client.api_call('chat.postMessage', channel=channel, text=sql_output, as_user=True)
    

class MainFunction(SlackCommunication):
    def __init__(self):
        super(MainFunction, self).__init__()
        
    def decideWhetherToTakeAction(self, input):
        if input:
            user, message, channel = input
            return self.writeToSlack(channel, message)
        
    def run(self):
        self.slackConnection()
        botID = self.getBotID(self.appName)
        while True:
            input = self.slackReadRTM()
            self.decideWhetherToTakeAction(self.parseSlackInput(input, botID))
            time.sleep(1)
            

if __name__ == '__main__':
    instance = MainFunction()
    instance.run()
