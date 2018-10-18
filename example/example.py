# -*- coding:utf-8 -*-

from cotoha_nlp.parse import Parser
import argparse
import pprint
import logging
logging.basicConfig(level=logging.DEBUG)

parser = argparse.ArgumentParser()
parser.add_argument("--client_id")
parser.add_argument("--client_secret")
parser.add_argument("--developer_api_base_url")
parser.add_argument("--access_token_publish_url")
args = parser.parse_args()
 
parser = Parser(args.client_id, args.client_secret, args.developer_api_base_url, args.access_token_publish_url)
s = parser.parse(input())
print(s.form)
print(s.get_root_chunk().form)
print(s.get_root_chunk().get_children(filter=["agent"])[0].get_chunk_head_token().form)

