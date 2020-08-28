import jieba
from collections import namedtuple
TermDocInfo = namedtuple('TermDocInfo', 'doc_id df')

class InvertedFile:
    def __init__(self, term_container, doc_word_count_info_list):
        self.term_id_to_index_list = []
        self.init_term_id_to_index_list(term_container)
        self.term_container = term_container
        self.build(doc_word_count_info_list)

    def init_term_id_to_index_list(self, term_container):
        for term_id in range(term_container.len()):
            self.term_id_to_index_list.append(InvertedIndex(term_id))
    
    def build(self, doc_word_count_info_list):
        for doc_word_count_info in doc_word_count_info_list:
            self.update(doc_word_count_info)
        self.set_tf()

    def update(self, doc_word_count_info):
        doc_id = doc_word_count_info.get_doc_id()
        for term, df in doc_word_count_info.items():
            term_id = self.term_container.get_term_id(term)
            inverted_index = self.get_inverted_index(term_id)
            inverted_index.append_doc_info(TermDocInfo(doc_id, df))

    def get_inverted_index(self, term_id):
        return self.term_id_to_index_list[term_id]

    def set_tf(self):
        for inverted_index in self.term_id_to_index_list:
            inverted_index.set_tf()

    def print(self):
        for term_id, index in enumerate(self.term_id_to_index_list):
            print(term_id, self.term_container.get_term_given_id(term_id), index.get_tf())
            index.print()

class InvertedIndex:
    def __init__(self, term_id):
        self.term_id = term_id
        self.doc_info_list = []
        self.tf = 0

    def append_doc_info(self, doc_info):
        self.doc_info_list.append(doc_info)

    def set_tf(self):
        self.tf = len(self.doc_info_list)

    def get_tf(self):
        return self.tf

    def print(self):
        for doc_info in self.doc_info_list:
            print(doc_info.doc_id, doc_info.df)

class DocWordCountInfo:
    def __init__(self, doc_id, review):
        self.doc_id = doc_id
        self.term_to_count_dict = {}
        self.build(review)

    def build(self, review):
        seg_list = jieba.cut_for_search(review)
        for term in seg_list:
            count = self.term_to_count_dict.get(term, 0)
            count = count + 1
            self.term_to_count_dict[term] = count

    def print(self):
        for term, df in self.term_to_count_dict.items():
            print(term, df)

    def keys(self):
        return self.term_to_count_dict.keys()

    def items(self):
        return self.term_to_count_dict.items()

    def get_doc_id(self):
        return self.doc_id
