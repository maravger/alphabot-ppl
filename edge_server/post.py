#!/usr/bin/env python
import requests
import json 

def main():
    
    post_url = "http://192.168.1.114:8000/"
    files  = {"file": open("./images/candidate1450.jpg", "rb")}
    r = requests.post(post_url, files=files )# , data=json)
    print (r.text)
    a = json.loads(r.text)
    print a[2] 
if __name__ == "__main__":
        main()
