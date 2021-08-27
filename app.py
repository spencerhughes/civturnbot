#!/usr/bin/env python3
from flask import Flask, json, request
import requests
import yaml
import logging

with open("config/config.yml", "r") as config_file:
	try:
		config = yaml.safe_load(config_file)
	except yaml.YAMLError as exc:
		app.logger.error(exc)

app = Flask(__name__)

@app.route('/', methods=['POST'])
def webhook():
	req = request.get_json()
	gameName = req['value1']
	try: 
		gameConf = config['webhooks'][gameName]
	except KeyError:
		error = { 'error': 'Game ' + gameName + ' not found.'}
		return error
	playerName = req['value2']
	try: 
		playerId = config['players'][playerName]
	except KeyError:
		error = { 'error': 'Player ' + str(playerName) + ' not found.'}
		return error
	turnNumber = req['value3']
	webhookUrl = gameConf['webhook']
	webhookType = gameConf['type']
	if webhookType == 'Discord':
		data = { "content":"<@" + str(playerId) + ">: it's your turn in " + gameName + " (Turn " + str(turnNumber) + ")" }
		hookreq = requests.post(webhookUrl, json=data)
	else:
		error = { "error": str(webhookType) + " is not a supported webhook type."}
		return error
	app.logger.info("New turn from " + gameName + ": Turn " + str(turnNumber) + ", Player " + playerName + " (ID: " + str(playerId) + ")")
	app.logger.info("Response code from " + webhookType + ": " + str(hookreq.status_code))
	return ("", 200, None)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
else:
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)