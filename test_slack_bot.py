import slack_bot
import pytest

input = [{'user': 'U9F9U2SJV', 'source_team': 'T9DT55SHE', 'team': 'T9DT55SHE', 'type': 'message', 'ts': '1522710309.000105', 'text': '<@U9GTU0MU7> test02', 'channel': 'D9F71S4KA'}]

@pytest.fixture
def initiateSlackCommunication():
    from slack_bot import SlackCommunication
    return SlackCommunication()

@pytest.fixture
def mainFunction():
    from slack_bot import MainFunction
    return MainFunction()

def test_slackConnection(initiateSlackCommunication):
    assert initiateSlackCommunication.slackConnection() == True

@pytest.mark.skip(reason="Not fully implemented")    
def test_slackReadRTM(initiateSlackCommunication):
    assert initiateSlackCommunication.slackReadRTM()
    
def test_parseSlackInput(initiateSlackCommunication):
    assert initiateSlackCommunication.parseSlackInput(input, 'U9GTU0MU7') == ['U9F9U2SJV', 'test02', 'D9F71S4KA']
    
def test_getBotID(initiateSlackCommunication):
    assert initiateSlackCommunication.getBotID('test-bot') == 'U9GTU0MU7'
    
def test_writeToSlack(initiateSlackCommunication):
    assert initiateSlackCommunication.writeToSlack('D9F71S4KA', 'Testing writing to slack')['ok'] == True
    
def test_decideWhetherToTakeAction_None(mainFunction):
    input = [None, None, None]
    assert mainFunction.decideWhetherToTakeAction(input)
    
def test_decideWhetherToTakeAction_Message(mainFunction):
    input = ['U9F9U2SJV', 'test03', 'D9F71S4KA']
    assert mainFunction.decideWhetherToTakeAction(input)