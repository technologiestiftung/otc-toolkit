#!/usr/bin/env python3.7

import requests
try:
  r = requests.get("http://localhost:8080/recording/start")
  print(r.status_code)
except Exception as e:
  print(e)