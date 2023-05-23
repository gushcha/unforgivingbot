#!/bin/bash

SCRIPTSDIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
BASEDIR=$(dirname $SCRIPTSDIR)
CONFIG_FILE_PATH="$BASEDIR/config.yml"

source "$SCRIPTSDIR/parse_yaml.sh"

eval $(parse_yaml $CONFIG_FILE_PATH "CONF_")

echo 'Creating db with configuration: '
echo "constainer:         $CONF_db_container"
echo "port:               $CONF_db_port"
echo "database:           $CONF_db_name"
echo "dbms password:      ${CONF_db_password_dbms:0:2}***"
echo "submitter password: ${CONF_db_password_submitter:0:2}***"
echo "notifier password:  ${CONF_db_password_notifier:0:2}***"


if (! docker stats --no-stream ); then
  >&2 echo "Docker not running exiting..."
  return
fi

mkdir -p data

docker start $CONF_db_container

if [ $? -ne 0 ]; then
    echo "Container unavailable, creating new $CONF_db_container"
    docker run --name $CONF_db_container -e POSTGRES_PASSWORD=$CONF_db_password_dbms -p $CONF_db_port:5432 -v "$BASEDIR/data:/var/lib/postgresql/data" -d postgres:15
fi

RETRIES=10
until docker exec $CONF_db_container sh -c 'pg_isready -U postgres' -eq 'accepting connections' || [ $RETRIES -eq 0 ]; do
    echo "Waiting for postgres server, $((RETRIES--)) remaining attempts..."
    sleep 3
done

if ! docker exec $CONF_db_container sh -c "psql -U postgres -lqt" | cut -d \| -f 1 | grep -qw $CONF_db_name; then
    docker exec $CONF_db_container sh -c "psql -U postgres -c 'CREATE DATABASE $CONF_db_name'"
    INIT_DB_SCRIPT_PATH="/var/lib/postgresql/init_script_$CONF_db_name.sql"
    docker cp $SCRIPTSDIR/db_init.sql $CONF_db_container:$INIT_DB_SCRIPT_PATH
    docker exec $CONF_db_container sh -c "psql -U postgres -d $CONF_db_name -f $INIT_DB_SCRIPT_PATH \
    -v password_db_submitter=\"'$CONF_db_password_submitter'\" -v password_db_notifier=\"'$CONF_db_password_notifier'\""
fi