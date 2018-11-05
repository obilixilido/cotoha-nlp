# -*- coding:utf-8 -*-

import os
import requests
import json

class CotohaAuth:
    def __init__(self, client_id:str, client_secret:str, access_token_publish_url:str, access_token:str = None):
        """ initialize
        Args:
            client_id (str): CLINED ID of COTOHA API
            client_secret (str): CLIENT SECRET of COTOHA API
            developer_api_base_url (str): Developer API Base URL of COTOHA API
            access_token_publish_url (str): Access Token Publicsh URL of COTOHA API
            access_token (str): Access token
        """
        if access_token != None:
            self.access_token = access_token
        else:
            self.client_id = client_id
            self.client_secret = client_secret
            self.access_token_publish_url = access_token_publish_url
            self.update_access_token()

    def update_access_token(self):
        """ update Access Token 
        TODO: use Requests-OAuthlib
        """
        if self.access_token_publish_url == None:
            raise RuntimeError("access_token_publish_url is not provided.")
        url = self.access_token_publish_url
        headers={
            "Content-Type": "application/json;charset=UTF-8"
        }
        data = {
            "grantType": "client_credentials",
            "clientId": self.client_id,
            "clientSecret": self.client_secret
        }
        data = json.dumps(data)
        response = requests.post(self.access_token_publish_url, headers=headers, data=data)
        response = json.loads(response.text)
        self.access_token = response["access_token"]



      
