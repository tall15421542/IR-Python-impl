import math
class TFIDF:
    def __init__(self, review_container):
        self.k1 = 1.0
        self.b = 0.75
        self.k3 = 500
        self.N = review_container.get_N()
        self.avdl = review_container.get_avdl()

    def get_tfidf_score(self, df, qtf, tf, dl):
        normalizer = self.get_normalizer(df)
        tf_score = self.get_tf_score(df, dl) 
        qtf_score = self.get_qtf_score(qtf) 
        return math.log(normalizer * tf_score * qtf_score) 

    def get_normalizer(self, df):
        return (self.N - df + 0.5) / (df + 0.5)

    def get_tf_score(self, tf, dl):
        return ((self.k1 + 1) * tf ) / (self.k1 * (1 - self.b + self.b * dl / self.avdl) + tf)

    def get_qtf_score(self, qtf):
        return ((self.k3 + 1) * qtf) / (self.k3 + qtf)

        

        

        
