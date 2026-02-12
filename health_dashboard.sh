#!/bin/bash

# Configuration
LB_URL="http://localhost"
DB_CONTAINER="triple-web-db-db-1"

while true; do
    clear
    echo "========================================================="
    echo "   DEV-OPS INFRASTRUCTURE MONITOR - TRIPLE-WEB-DB"
    echo "========================================================="
    echo "TIME: $(date)"
    echo "---------------------------------------------------------"
    
    # 1. Check which site is currently ACTIVE via Load Balancer
    ACTIVE_SITE=$(curl -s --max-time 1 $LB_URL | grep -oE "ALPHA|BETA|GAMMA" | head -n 1)
    if [ -z "$ACTIVE_SITE" ]; then
        ACTIVE_SITE="OFFLINE (CRITICAL)"
    fi
    echo -e "CURRENT LIVE TRAFFIC ROUTE: \033[1;32m$ACTIVE_SITE\033[0m"
    echo "---------------------------------------------------------"

    # 2. Display Docker Resource Usage (Standard Compatible Fields)
    echo "CONTAINER RESOURCE UTILIZATION:"
    docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}\t{{.NetIO}}"
    
    echo "---------------------------------------------------------"
    # 3. Check Database Connection
    DB_STATUS=$(docker exec $DB_CONTAINER mariadb-admin ping -uuser -ppassword 2>/dev/null)
    if [[ $DB_STATUS == *"mysqld is alive"* ]]; then
        echo -e "DATABASE STATUS: \033[1;32mCONNECTED\033[0m"
    else
        echo -e "DATABASE STATUS: \033[1;31mDISCONNECTED\033[0m"
    fi
    
    echo "---------------------------------------------------------"
    echo "Press [CTRL+C] to exit dashboard..."
    sleep 2
done
