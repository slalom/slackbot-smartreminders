#!/bin/bash

# environment variables SLACK_BOT_TOKEN and SLACK_VERIFICATION_TOKEN needed
# to set up heroku app
if [[ -z "$SLACK_BOT_TOKEN" ]]; then
	echo "SLACK_BOT_TOKEN is required but not set in your local environment"
	exit 1
elif [[ -z "$SLACK_VERIFICATION_TOKEN" ]]; then
	echo "SLACK_VERIFICATION_TOKEN is required but not set in your local environment"
	exit 1
fi

echo "Requirements fufilled..."

# first, make sure we are on the master branch
git checkout master

# Check whether our local master branch is in sync with the remote master
LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse @{u})
BASE=$(git merge-base @ @{u})

if [ "$LOCAL"=="$REMOTE" ]; then
    echo "Working branch is up-to-date with remote master, proceeding...."
elif [ "$LOCAL"=="$BASE" ]; then
    echo -e "Your working branch is behind the remote branch, you need to run:\ngit pull"
    exit 1
elif [ "$REMOTE"=="$BASE" ]; then
    echo -e "Your working branch is ahead of the remote branch, you need to run:\ngit push origin master"
    exit 1
else
    echo "Your working branch has diverged from the remote master, cannot continue"
    exit 1
fi

BRANCH_NAME=$1

# branch may exist already locally or remotelly
if [ `git branch | egrep "^\*?[[:space:]]+(remotes\/origin\/)?${BRANCH_NAME}$"` ]; then
    echo "The branch ${BRANCH_NAME} already exists!"
	exit 1
fi

# create development branch
git checkout -b $BRANCH_NAME

# create the development heroku instance
# format: PIPELINE-BRANCH_NAME
APP_NAME="smartreminders-${BRANCH_NAME}"

# heroku apps cannot be longer than 30 characters
until [[ ${#APP_NAME} -le 30 ]]; do
	echo "Heroku App name ${APP_NAME} is too long!"
	read -p "Please enter an alternative app name: " APP_SLUG
	APP_NAME="smartreminders-${APP_SLUG}"
done

echo "Creating Heroku app ${APP_NAME}..."

# heroku remote is named after the branch to keep it unique
results="$(heroku create --app $APP_NAME  2>&1)"

# check heroku error message
if [[ `echo ${results} | egrep "Name ${APP_NAME} is already taken"` ]]; then
	echo "Heroku application already exists"
	exit 1
fi

# configure git remote to point to heroku deployment
heroku git:remote -r ${BRANCH_NAME} -a ${APP_NAME}

# set the required environment variables 
heroku config:set SLACK_BOT_TOKEN=$SLACK_BOT_TOKEN -a $APP_NAME
heroku config:set SLACK_VERIFICATION_TOKEN=$SLACK_VERIFICATION_TOKEN -a $APP_NAME

# add the app to the development pipeline
heroku pipelines:add smartreminders -a $APP_NAME

echo "Successfully created!

Branch Name: ${BRANCH_NAME}
Git Remote: ${BRANCH_NAME}
Heroku App Name: ${APP_NAME}
Response URL: https://${APP_NAME}.herokuapp.com"