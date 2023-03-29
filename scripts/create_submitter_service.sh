#!/bin/bash
# RUN as sudo

SCRIPTSDIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
BASEDIR=$(dirname $SCRIPTSDIR)
CONFIG_FILE_PATH="$BASEDIR/config.yml"
PYTHON_EXECUTOR="$BASEDIR/venv/bin/python"
PYTHON_EXECUTABLE="start_submitter.py"

source $SCRIPTSDIR/parse_yaml.sh

eval $(parse_yaml $CONFIG_FILE_PATH "CONF_")

SERVICE_DESCRIPTION="service $CONF_bot_name"
SERVICE_FILE_NAME="$CONF_bot_name.service"

read -r -d '' SERVICE_CONFIG <<- EOM
[Unit]
Description=$SERVICE_DESCRIPTION
After=multi-user.target
[Service]
User=$CONF_user
Type=simple
Restart=always
WorkingDirectory=$BASEDIR
ExecStart=$PYTHON_EXECUTOR $PYTHON_EXECUTABLE
[Install]
WantedBy=multi-user.target
EOM

echo $"$SERVICE_CONFIG" > "/etc/systemd/system/$SERVICE_FILE_NAME"