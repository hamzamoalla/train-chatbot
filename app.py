from flask import Flask, render_template, jsonify, request
import requests

rasa_api_url='http://localhost:5005/webhooks/rest/webhook'

app = Flask(__name__)

@app.get("/")
def index_get():
    return render_template("base.html")

@app.route('/webhook', methods=['POST'])
def webhook():
    user_message = request.json['message']
    print("User Message:", user_message)
    rasa_response = requests.post(rasa_api_url, json={'message': user_message})
    rasa_response_json = rasa_response.json()
    print("Rasa Response:", rasa_response_json)
    bot_responses = [message['text'] for message in rasa_response_json if 'text' in message]
    return jsonify({'response': bot_responses})

if __name__=="__main__":
    app.run(debug=True, port=3000)
