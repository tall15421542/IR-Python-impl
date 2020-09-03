class ReviewContainer:
    def __init__(self, sheet):
        self.review_list = []
        self.N = 0
        self.avdl = 0
        self.build(sheet)

    def build(self, sheet):
        for col in sheet.iter_rows(min_row = 2, min_col = 8, max_col = 8, values_only = True):
            review = col[0]
            if review:
                self.review_list.append(review.upper())
        self.set_N()
        self.set_avdl()

    def set_N(self):
        self.N = len(self.review_list)

    def get_N(self):
        return self.N

    def set_avdl(self):
        total_len = 0
        for review in self.review_list:
            total_len += len(review)
        self.avdl = total_len / self.N
    
    def get_dl_given_doc_id(self, doc_id):
        return len(self.review_list[doc_id])

    def get_avdl(self):
        return self.avdl

    def get_review_list(self):
        return self.review_list

    def get_review(self, review_id):
        return self.review_list[review_id]

class ReviewAccumulatorDict:
    def __init__(self, inverted_file, tfidf_engine, review_container):
        self.inverted_file = inverted_file
        self.tfidf_engine = tfidf_engine
        self.doc_id_to_review_accumulator_dict = {}
        self.review_container = review_container

    def update(self, qtf, term):
        if self.inverted_file.is_exist(term):
            term_id = self.inverted_file.get_term_id(term)
            inverted_index = self.inverted_file.get_inverted_index(term_id)
            self.update_doc_id_to_review_accumulator_dict(qtf, inverted_index)

    def update_doc_id_to_review_accumulator_dict(self, qtf, inverted_index):
        df = inverted_index.get_df()
        for doc_info in inverted_index.get_doc_info_list():
            doc_id = doc_info.doc_id
            dl = self.review_container.get_dl_given_doc_id(doc_id)
            tf = doc_info.tf
            review_accumulator = self.doc_id_to_review_accumulator_dict.get(doc_id, ReviewAccumulator(doc_id))
            review_accumulator.update_score(self.tfidf_engine.get_tfidf_score(df, qtf, tf, dl))
            self.doc_id_to_review_accumulator_dict[doc_id] = review_accumulator

    def values(self):
        return self.doc_id_to_review_accumulator_dict.values()

    def print(self):
        for doc_id, review_accumulator in self.doc_id_to_review_accumulator_dict.items():
            print(doc_id, review_accumulator.get_score())

class ReviewAccumulator:
    def __init__(self, doc_id):
        self.doc_id = doc_id
        self.score = 0.
   
    def update_score(self, score):
        self.score += score

    def get_score(self):
        return self.score

    def get_doc_id(self):
        return self.doc_id

    def __lt__(self, other):
        return self.score < other.score
