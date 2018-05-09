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
        self.appName = 'data-bot'
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
            error_message = 'I did not understand it. Please try again.'
            message = html.unescape(message)
            print('input from slack --------------->>>>', message)
            print('input type from slack --------------->>>>', type(message))
            # sql_output = self.db.fetch_data(message)
            output_dict = self.user_input_utility.fetch_response_from_model(message) 
            attachment = {'fields':[{}]}
            column_names = ["Player", "No.", "Nationality", "Position", \
                            "Years in Toronto", "School/Club Team"]
            if output_dict['value'] == [] or len(message.split()) == 1:
                # sql_output = 'I did not understand it. Please try again.
                return self.slack_client.api_call('chat.postMessage', channel=channel, text = error_message, as_user=True)
            else:
                value_str = ""
                for output in output_dict['value']:
                    value_str += output + "\n"
                    
                attachment['fields'][0]['title'] = column_names[output_dict['col_index']]
                attachment['fields'][0]['value'] = value_str
                return self.slack_client.api_call('chat.postMessage', channel=channel, attachments=[attachment], as_user=True)  
            
    

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
