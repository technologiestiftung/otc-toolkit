#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests

url = "http://192.168.1.209:8080/counter/areas"

payload = "{\"countingAreas\":{  \"5287124a-4598-44e7-abaf-394018a7278b\": {\"color\": \"yellow\",\"location\": {  \"point1\": {\"x\": 221,\"y\": 588 },\"point2\": {\"x\": 673,\"y\": 546},  \"refResolution\": {\"w\": 1280,\"h\": 666  }},\"name\": \"Counter line 1\",\"type\": \"bidirectional\"}}}"
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data = payload)

print(response.text.encode('utf8'))


