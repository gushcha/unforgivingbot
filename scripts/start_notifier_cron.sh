#!/bin/bash
# RUN as sudo

SCRIPTSDIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
BASEDIR=$(dirname $SCRIPTSDIR)
CONFIG_FILE_PATH="$BASEDIR/config.yml"

source $SCRIPTSDIR/parse_yaml.sh

eval $(parse_yaml $CONFIG_FILE_PATH "CONF_")

echo "*/$(($CONF_notifier_runtime_delta/60)) * * * *  cd $BASEDIR && ./venv/bin/python start_notifier.py" | crontab -u $CONF_user -