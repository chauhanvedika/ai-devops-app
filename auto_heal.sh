#!/bin/bash

echo "🔍 Checking AI system status..."

STATUS=$(curl -s http://localhost:5000/metrics | grep ai_system_status | awk '{print $2}')

echo "Current status: $STATUS"

if [ "$STATUS" = "2" ]; then
    echo "🚨 Critical issue detected! Restarting container..."

    docker restart ai-app

    echo "✅ Container restarted"
else
    echo "✅ System healthy"
fi