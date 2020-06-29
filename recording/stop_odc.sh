#!/bin/sh
cd /home/otc-xavier/opendatacam

#Stop ODC - use pm2 to run in the background
pm2 stop server.js 

