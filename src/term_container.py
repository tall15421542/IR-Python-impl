class TermContainer:
    def __init__(self, doc_word_count_info_list):
        self.id_to_term_list = []
        self.term_to_id_dict = {}
        self.build(doc_word_count_info_list)

    def build(self, doc_word_count_info_list):
        for doc_word_count_info in doc_word_count_info_list:
            self.update(doc_word_count_info)

    def len(self):
        return len(self.id_to_term_list)

    def update(self, doc_word_count_info):
        for word in doc_word_count_info.keys():
            self.update_term(word)

    def update_term(self, term):
        if self.is_exist(term):
            return
        self.add_term(term)

    def is_exist(self, term):
        if term in self.term_to_id_dict:
            return True
        else:
            return False

    def add_term(self, term):
        self.term_to_id_dict[term] = len(self.id_to_term_list)
        self.id_to_term_list.append(term)

    def get_term_id(self, term):
        return self.term_to_id_dict.get(term)

    def get_term_given_id(self, term_id):
        return self.id_to_term_list[term_id]

    def print(self):
        for term_id, term in enumerate(self.id_to_term_list):
            print(term_id, term)
        for term, term_id in self.term_to_id_dict.items():
            print(term, term_id)

