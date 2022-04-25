#!/bin/bash
echo Starting Good Mood server...
cd /var/www/budget101/server/
gunicorn -w 6 -b 127.0.0.1:5015 server:app --timeout 600
