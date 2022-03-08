# coding: utf-8
# Author: Siwanont Sittinam

import os
from requests import request
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv()


class PrismaCloudAuthentication:
    def getHostname(self):
        HOSTNAME = os.getenv("prismaCloudURL")
        return HOSTNAME

    def getSessionTime(self):
        given_time = datetime.now()
        final_time = given_time + timedelta(minutes=10)

        print(f"Created Time : %s\nExpired Time : %s" % (given_time.strftime('%Y-%m-%d %H:%M:%S'), final_time.strftime('%Y-%m-%d %H:%M:%S')))
        print("Duration : 10 Minutes")

    def login(self):
        BASE_URL = self.getHostname()
        loginURL = str(BASE_URL) + "/login"

        HEADERS = {"content-type": "application/json; charset=UTF-8"}

        ACCESS_ID = os.getenv("ACCESS_ID")
        ACCESS_KEY = os.getenv("ACCESS_KEY")

        payload = {
            "username": str(ACCESS_ID),
            "password": str(ACCESS_KEY)
        }

        r = request("POST", loginURL, json=payload, headers=HEADERS)
        if r.status_code == 200:
            r = r.json()
            print("Getting Token Successful")
            self.getSessionTime()
            return r["token"]
        print(f'[%d] %s' % (r.status_code, r.json()["message"]))
        return None

    def extendSession(self, TOKEN=""):
        # Generate New Token
        BASE_URL = self.getHostname()
        extendSessionurl = str(BASE_URL) + "/auth_token/extend"

        HEADERS = {
            "content-type": "application/json",
            "x-redlock-auth": str(TOKEN)
        }

        r = request("GET", extendSessionurl, headers=HEADERS)
        if r.status_code == 200:
            r = r.json()
            print("Getting Token Successful")
            self.getSessionTime()
            return r["token"]
        print(f'[%d] %s' % (r.status_code, r.text))
        return None
