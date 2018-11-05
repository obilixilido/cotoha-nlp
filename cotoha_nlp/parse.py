# -*- coding:utf-8 -*-

import os
import requests
import json

from .data.sentence import Sentence
from .auth import CotohaAuth

class Parser:
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
 
    def parse(self, sentence: str, param: dict = {}):
        """ Call Parse API 
        Args:
            sentence (str): target sentence
            param (dict): parameter of parse API. see https://api.ce-cotoha.com/contents/reference.html#api-Parse
        Return:
           sentence object 
        """
        data = {
            "sentence": sentence
        }
        data.update(param)
        data = json.dumps(data)
        try:
            with requests.post(self.developer_api_base_url + "/v1/parse", headers=self.make_header(), data=data) as res:
                sentence = Sentence(sentence, json.loads(res.text)["result"])
                for chunk in sentence.chunks:
                    chunk.set_sentence(sentence)
                    for token in chunk.tokens:
                        token.set_sentence(sentence)
                return sentence
        except requests.exceptions.RequestException as e:
            # FIXME
            raise e
