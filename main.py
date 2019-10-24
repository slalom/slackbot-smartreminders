import os
import slack
import json
import asyncio
from flask import Flask, jsonify, abort, request, make_response
from datetime import datetime, timedelta
from slack.errors import SlackClientError
from utils import parse_command

SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
client = slack.WebClient(token=SLACK_BOT_TOKEN, run_async=True)

loop = asyncio.new_event_loop()
app = Flask(__name__)


# def queue_messages():
# 	current_time = datetime.now()
# 	for i in range(4):
# 		current_time = current_time + timedelta(minutes=1)
# 		client.chat_scheduleMessage(
# 			channel="#general",
# 			text="@channel hello",
# 			post_at=current_time.strftime("%s")
# 		)

def is_request_valid(request):
	is_token_valid = request.form['token'] == os.environ['SLACK_VERIFICATION_TOKEN']
	return is_token_valid



# /list: lists all the currently active reminders
@app.route("/commands/list", methods=["POST"])
def listCommand():
	try:
		asyncio.set_event_loop(loop)
		response = loop.run_until_complete(client.chat_scheduledMessages_list(
			channel=request.form['channel_id']
		))

		if (response['scheduled_messages'] == []):
			return jsonify(
				response_type="in_channel",
				text="There are currently no scheduled reminders."
			)
		
		return jsonify(
			response_type="in_channel",
			text=response['scheduled_messages']
		)
	except SlackClientError:
		return jsonify(
			response_type="in_channel",
			text=response["error"]
		)

# /add: add a monthly reminder (schedules it for 120 days due to the limitations
# 			of the slack command chat.scheduleMessages)
@app.route('/commands/add', methods=["POST"])
def addCommand():
	try:
		asyncio.set_event_loop(loop)

		dates = parse_command(request.form["text"])

		print(dates)

		for date in dates:
			response = loop.run_until_complete(client.chat_scheduleMessage(
				channel="CP9V91V3N",
				post_at=date,
				text="test reminder"
			))

			print(type(response))

		return jsonify(
			response_type="in_channel",
			text=response['ok']
		)

	except SlackClientError:
		return jsonify(
			response_type="in_channel",
			text=response['error']
		)

if __name__ == "__main__":
	app.run(debug=True)