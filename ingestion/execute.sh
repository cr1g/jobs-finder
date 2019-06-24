#!/bin/bash

set -e

echo "Wait for MySQL container to start..."
sleep 30

python rabota.py
