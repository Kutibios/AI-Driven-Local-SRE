#!/bin/bash
ERRORS=(
  "CRITICAL: Memory leak detected in process 4501. Usage above 95%."
  "ERROR: Connection timeout while reaching api.auth.service:8080"
  "ERROR: Permission denied (Public key) for user 'root' on server node-03"
  "CRITICAL: Disk I/O failure on /dev/sda1. System entering read-only mode."
)

RANDOM_ERROR=${ERRORS[$RANDOM % ${#ERRORS[@]}]}
echo "[ERROR] $(date '+%Y-%m-%d %H:%M:%S') - $RANDOM_ERROR" >> logs/test.log