#importing necessary libraries
import json
from urllib.request import urlopen, Request

#Function to add two numbers
def add(a, b):
    return a + b

#Function to fetch JSON data from a URL
def fetch_json(url):
    req = Request(url, headers={'User-Agent': 'Python'})
    with urlopen(req) as response:
        return json.load(response)
