import random
from flask import Flask, request
from pymessenger.bot import Bot
import os

app = Flask(__name__, static_url_path='')
port = int(os.getenv('PORT', 8000))

ACCESS_TOKEN = 'EAAX5iE28QIgBALFWiNWGIuZCpgBzET4UcXZCkDg2m8G5yiTdcUsEib9HKxtb6iTLKfbAv3kFA6tl8XG5laOey8A3mWoh8Sz4lzhiFC2F3Lkm5IowjKejU0aA5mYlLnDQYpP6gZCphA0bLXgmJ5V7CCxUUkUkxXzm1KR7sKHFQZDZD'
VERIFY_TOKEN = 'V3rySaf3AndL0ngT00ken'
bot = Bot(ACCESS_TOKEN)

#We will receive messages that Facebook sends our bot at this endpoint 
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook.""" 
        token_sent = request.args.get("hub.verify_token")
        if token_sent is None:
            return "Hello World"
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot
       output = request.get_json()
       for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            if message.get('message'):
                #Facebook Messenger ID for user so we know where to send response back to
                recipient_id = message['sender']['id']
                if message['message'].get('text'):
                    response_sent_text = message['message'].get('text') + " Its chatbot here "
                    send_message(recipient_id, response_sent_text)
                #if user sends us a GIF, photo,video, or any other non-text item
                if message['message'].get('attachments'):
                    response_sent_nontext = get_message() + " Its chatbot here you have sent attachments"
                    send_message(recipient_id, response_sent_nontext)
    return "Message Processed"


def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error 
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


#chooses a random message to send to the user
def get_message():
    sample_responses = ["You are stunning!", "We're proud of you.", "Keep on being you!", "We're greatful to know you :)"]
    # return selected item to the user
    return random.choice(sample_responses)

#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)