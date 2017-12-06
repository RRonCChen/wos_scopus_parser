class Paper:
    def __init__(self,title,authors,sourceTitle,date,JCR_detail,cite_count,citation_papers):
        self.title = title
        self.authors = authors
        self.sourceTitle = sourceTitle
        self.date = date
        self.JCR_detail = JCR_detail
        self.cite_count = cite_count
        self.citation_papers = citation_papers

        def get_title(self):
            return self.title

        def set_title(self, title):
            self.title = title

        def set__authors(self,authors):
            self.authors= authors

        def get__authors(self):
            return self.authors

        def get_sourceTitle(self):
            return self.sourceTitle

        def set_sourceTitle(self, sourceTitle):
            self.sourceTitle = sourceTitle

        def get_date(self):
            return self.date

        def set_date(self, date):
            self.date = date

        def get_JCR_detail(self):
            return self.JCR_detail

        def set_JCR_detail(self, JCR_detail):
            self.JCR_detail= JCR_detail

        def get_cite_count(self):
            return self.cite_count

        def set_cite_count(self, cite_count):
            self.cite_count = cite_count

        def get_citation_papers(self):
            return self.citation_papers

        def set_citation_papers(self, citation_papers):
            self.citation_papers = citation_papers


class Citation:
    def __init__(self,title,sourceTitle,date,JCR_detail,cite_count):
        self.title = title
        self.sourceTitle = sourceTitle
        self.date = date
        self.JCR_detail = JCR_detail
        self.cite_count = cite_count

        def get_title(self):
            return self.title

        def set_title(self, title):
            self.title = title

        def get_sourceTitle(self):
            return self.sourceTitle

        def set_sourceTitle(self, sourceTitle):
            self.sourceTitle = sourceTitle

        def get_date(self):
            return self.date

        def set_date(self, date):
            self.date = date

        def get_JCR_detail(self):
            return self.JCR_detail

        def set_JCR_detail(self, JCR_detail):
            self.JCR_detail = JCR_detail

        def get_cite_count(self):
            return self.cite_count

        def set_cite_count(self, cite_count):
            self.cite_count = cite_count