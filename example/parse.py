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

# 入力文そのまま
print(s.form)
# 述語の文節の表記を取得
print(s.get_predicate().form)
# 述語の動作主を取得
print(s.get_predicate().get_children(filter=["agent"])[0].get_chunk_head_token().form)
# 述語の動作主を形容している語を取得
print(s.get_predicate().get_children(filter=["agent"])[0].get_chunk_head_token().get_children(filter=["nomd"])[0].form)
