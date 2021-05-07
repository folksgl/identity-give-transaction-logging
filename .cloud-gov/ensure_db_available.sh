#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: $0 CF_SERVICE_NAME"
    exit 1
fi

cf_service_name=$1

# Waits for the cf service status to become create/update succeeded
wait_for_service_creation() {
    time_limit=600 # 10 minutes

    while [ $time_limit -ne 0 ] && [ -z "$service_status" ]; do
        echo "Waiting for service to become available. Seconds before timeout: $time_limit"
        sleep 30
        time_limit=$((time_limit - 30))
        service_status=$(cf service "$cf_service_name" | grep "status:" | grep "create succeeded\|update succeeded")
    done

    # If the service still isn't available, fail the script
    if [ -z "$service_status" ]; then
        echo "DB failed to become ready within the time limit."
        exit 1
    fi

    echo "DB creation finalized"
}

create_db() {
    service_plan="micro-psql"
    cf create-service aws-rds $service_plan "$cf_service_name"
}

# Test if DB service exists at all
if ! cf services | grep --silent "^$cf_service_name "; then
    echo "Unable to find database service: $cf_service_name. Creating..."
    create_db
    wait_for_service_creation
    exit 0
fi

# The DB service existed, but the service status is not yet known
echo "Found service $cf_service_name. Checking service status..."

db_status=$(cf service "$cf_service_name" | grep "status:")

db_succeeded=$(echo "$db_status" | grep "create succeeded\|update succeeded")
db_in_progress=$(echo "$db_status" | grep "in progress")

if [ -n "$db_succeeded" ]; then
    echo "DB already available"
elif [ -n "$db_in_progress" ]; then
    echo "DB creation was "in progress"."
    wait_for_service_creation
else
    # Status was neither "in progress" or "create|update succeeded". There's likely
    # a problem with the DB service that can't be resolved without human interaction
    echo "Found DB service: $cf_service_name but status was: $db_status"
    exit 1
fi
