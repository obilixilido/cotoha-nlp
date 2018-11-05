# -*- coding:utf-8 -*-

import os
import requests
import json

from .data.sentence import Sentence
from .auth import CotohaAuth

class Similarity:
    def __init__(self, client_id:str, client_secret:str, developer_api_base_url:str, access_token_publish_url:str, access_token:str = None):
        """ initialize
        Args:
            client_id (str): CLINED ID of COTOHA API
            client_secret (str): CLIENT SECRET of COTOHA API
            developer_api_base_url (str): Developer API Base URL of COTOHA API
            access_token_publish_url (str): Access Token Publicsh URL of COTOHA API
            access_token (str): Access token
        """
        self.auth_info = CotohaAuth(client_id=client_id, client_secret=client_secret, 
            access_token_publish_url=access_token_publish_url, 
            access_token=access_token)
        self.developer_api_base_url = developer_api_base_url

    def make_header(self):
        return {
            "Authorization": "Bearer " + self.auth_info.access_token,
            "Content-Type": "application/json;charset=UTF-8",
        }
 
    def calc_similarity(self, sentence_1: str, sentence_2: str, param: dict = {}):
        """ Call Similarity API 
        Args:
            sentence_1 (str): target sentence
            sentence_2 (str): target sentence
            param (dict): parameter of parse API. see https://api.ce-cotoha.com/contents/reference.html#api-Similarity
        Return:
           sentence object 
        """
        data = {
            "s1": sentence_1,
            "s2": sentence_2
        }
        data.update(param)
        data = json.dumps(data)
        try:
            with requests.post(self.developer_api_base_url + "/v1/similarity", headers=self.make_header(), data=data) as res:
                return json.loads(res.text)["result"]["score"]
        except requests.exceptions.RequestException as e:
            # FIXME
            if(res.status_code == 401):
                # retry if auth error
                self.auth_info.update_access_token()
                return calc_similarity(sentence_1, sentence_2, param)
            raise e
