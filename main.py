import os
import slack
import json
import asyncio
import itertools
from flask import Flask, jsonify, abort, request, make_response
from datetime import datetime, timedelta
from slack.errors import SlackClientError
from utils import parse_command

SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
client = slack.WebClient(token=SLACK_BOT_TOKEN, run_async=True)

loop = asyncio.new_event_loop()
app = Flask(__name__)

def is_request_valid(request):
	is_token_valid = request.form['token'] == os.environ['SLACK_VERIFICATION_TOKEN']
	return is_token_valid

# def collapse_scheduled_messages(messages):
# 	# iter(messages)
# 	unique_messages = list({v['text']: v for v in messages}.values())
# 	return unique_messages


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

		# unique_messages = collapse_scheduled_messages(response['scheduled_messages'])
		# print('all messages',len(response['scheduled_messages']))
		# print('unique messages', len(unique_messages))

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

		command = parse_command(request.form['text'])
		text = command.get('text')
		dates = command.get('scheduled_dates')

		# print(dates[-1])

		# last_date=datetime.fromtimestamp(int(dates[-1]))
		# last_reminder = datetime.strftime(last_date, '%B %d, %Y')

		for date in dates:
			response = loop.run_until_complete(client.chat_scheduleMessage(
				channel="CP9V91V3N",
				post_at=date,
				text=text
			))

		return jsonify(
			response_type="in_channel",
			text="Successfully Added!",
			# blocks=[
			# 	{
			# 		"type": "section",
			# 		"text": {
			# 			"type": "plain_text",
			# 			"text": "Reminder: " + text
			# 		}
			# 	},
			# 	{
			# 		"type": "context",
			# 		"elements": [
			# 			{
			# 				"type": "mrkdwn",
			# 				"text": "Good until " + last_reminder
			# 			}
			# 		]
			# 	}
			# ]
		)

	except SlackClientError:
		return jsonify(
			response_type="in_channel",
			text=response['error']
		)

if __name__ == "__main__":
	app.run(debug=True)