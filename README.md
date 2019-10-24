# SmartReminders Slackbot

Extending the ability to create reminders on a monthly basis (MVP)

## Requirements

* A slack account (preferrably using your slalom email)
* A heroku account (managing instances of the slack app, manage environment variables, etc)

## Setup

### Slack

* The SmartReminders Slackbot is currently only available through a bare slack workspace, so to test/use it, you'll need access
  * [Abby's Test Bots](https://abby-test-bots.slack.com)
* Once you have access, reach out to Abby Bashore so she can add you as a collaborator for the slack app
* After you have collaborator access, you will be able to access tokens, add slash commands, etc.
  * [SmartReminders App](https://api.slack.com/apps/APB5BF3PT)

### Heroku Deployment

1. If you have an heroku account, please contact Abby Bashore so she can add you as a collaborator on the heroku instance
2. clone the repository (if you haven't done it yet)
3. `cd slackbot-smartreminders/`

Once you are logged in and ready to develop, see the note about the `generate-dev-env` script below.

Keep in mind that you may have to run `git pull --rebase` in case another developer deploys the application and it is not updated

## Important Notes

### Working with the Heroku Pipeline

Each slash command requires a response URL that will consume the requests. Currently, the production code points to the heroku app (https://smartreminders.herokuapp.com/).
To test slash commands currently in development, a seperate heroku app needs to be created, such that your development code points to a seperate url (e.g. https://smartreminders-branch-name.herokuapp.com/). The bash script generate-dev-env.sh automates this for you. 

Before creating a development branch, run: `./generate-dev-env.sh {YOUR_BRANCH_NAME}` with your branch name.

This will: 
 * create a branch off of the master branch 
 * create a heroku app
 * sets the environment variables needed to call the slack bot
 * add it to the smartreminders pipeline in the development stage

Pushing to the development app that was created:
  1. stage your commits with git
  2. `git push {BRANCH_NAME} {BRANCH_NAME}:master`

Testing your development code:
  1. Go to the [SmartReminders App](https://api.slack.com/apps/APB5BF3PT)
  2. add a slash command corresponding to the slash command you want to test
  3. enter the response url that points to your development code