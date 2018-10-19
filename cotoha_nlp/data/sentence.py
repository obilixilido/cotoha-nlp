# -*- coding:utf-8 -*-

import json
import pprint

class Sentence:
    """ Sentence class """
    def __init__(self, form: str, data: list):
        self.form = form
        self.chunks = [chunk for chunk_and_tokens in data for chunk in [Chunk(chunk_and_tokens)]]
        self.tokens = [token for chunk in self.chunks for token in chunk.tokens]

    def get_root_chunk(self):
        return [chunk for chunk in self.chunks if chunk.dep == "O"][0]

    def get_predicate(self):
        return self.get_root_chunk()

    def __str__(self):
        return(json.dumps([chunk.to_json() for chunk in self.chunks], ensure_ascii=False))

    def __repr__(self):
        return self.__str__()

class Chunk:
    """ Chunk class """
    def __init__(self, data: dict):
        self.chunk = data["chunk_info"]
        self.id = data["chunk_info"]["id"]
        self.head = data["chunk_info"]["head"]
        self.dep = data["chunk_info"]["dep"]
        self.chunk_head = data["chunk_info"]["chunk_head"]
        self.chunk_func = data["chunk_info"]["chunk_func"]
        self.links = data["chunk_info"]["links"]
        self.tokens = [token for token_json in data["tokens"] for token in [Token(token_json)]]
        self.form = "".join([token.form for token in self.tokens])

    def set_sentence(self, sentence: Sentence):
        self.sentence = sentence

    def get_head_token(self):
        return self.sentence.tokens[self.head]

    def get_chunk_head_token(self):
        return self.tokens[self.chunk_head]

    def get_chunk_func_token(self):
        return self.tokens[self.chunk_func]

    def get_children(self, filter: list = []):
        if len(filter) == 0:
            return [self.sentence.chunks[link["link"]] for link in self.links]
        else:
            return [self.sentence.chunks[link["link"]] for link in self.links if link["label"] in filter]

    def get_parent(self):
        for chunk in self.sentence.chunks:
            if self.id in [link["link"] for link in chunk.links]:
                return chunk
        # no child don't have parent!

    def __str__(self):
        return(json.dumps({
            "chunk_info": self.chunk, 
            "tokens": [token.to_dict() for token in self.tokens]}, ensure_ascii=False))

    def __repr__(self):
        return self.__str__()

    def to_json(self):
        return self.__repr__()
           

class Token:
    """ Token class """
    def __init__(self, data: dict):
        self.form = data["form"]
        self.lemma = data["lemma"]
        self.kana = data["kana"]
        self.id = data["id"]
        self.pos = data["pos"]
        self.features = data["features"]
        self.dependency_labels = data["dependency_labels"] if "dependency_labels" in data else {}
        self.attributes = data["attributes"]

    def set_sentence(self, sentence: Sentence):
        self.sentence = sentence

    def get_children(self, filter: list = []):
        return [self.sentence.tokens[deps["token_id"]] for deps in self.dependency_labels]
        if len(filter) == 0:
            return [self.sentence.tokens[deps["token_id"]] for deps in self.dependency_labels]
        else:
            return [self.sentence.tokens[deps["token_id"]] for deps in self.dependency_labels in deps["label"] in filter]

    def get_parent_token(self):
        # FIXME
        pass

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return(json.dumps(self.to_dict(), ensure_ascii=False))

    def to_json(self):
        return self.__repr__();

    def to_dict(self):
        return {
            "id": self.id,
            "form": self.form, 
            "lemma": self.lemma,
            "kana": self.kana,
            "pos": self.pos,
            "feautes": self.features,
            "dependency_labels": self.dependency_labels,
            "attributes": self.attributes
        }
