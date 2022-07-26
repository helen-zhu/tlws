import requests
import pandas as pd

response = requests.get("http://localhost:8080/test.html")
print("status code:", response.status_code)
print("content length:", response.headers["content-length"])
print(response.text)

files = {'file': open('test.csv', 'rb')}
response = requests.post("http://localhost:8080", files = files)
print("status code:", response.status_code)
print("content length:", response.headers["content-length"])
print(response.text)
