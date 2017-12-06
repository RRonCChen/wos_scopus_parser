class Paper:
    def __init__(self,authors,title,date,sourceTitle,cite_count,citation_papers,type):
        self.title = title
        self.authors = authors
        self.sourceTitle = sourceTitle
        self.date = date
        self.cite_count = cite_count
        self.citation_papers = citation_papers
        self.type = type

    def get_title(self):
        return self.title

    def set_title(self, title):
        self.title = title

    def set__authors(self, authors):
        self.authors = authors

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

    def get_cite_count(self):
        return self.cite_count

    def set_cite_count(self, cite_count):
        self.cite_count = cite_count

    def get_citation_papers(self):
        return self.citation_papers

    def set_citation_papers(self, citation_papers):
        self.citation_papers = citation_papers

    def get_type(self):
        return self.type

    def set_type(self, type):
        self.type = type

class Citation:
    def __init__(self,authors,title,sourceTitle,date,cite_count):
        self.title = title
        self.sourceTitle = sourceTitle
        self.authors = authors
        self.date = date
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

        def get_cite_count(self):
            return self.cite_count

        def set_cite_count(self, cite_count):
            self.cite_count = cite_count

        def set__authors(self, authors):
            self.authors = authors

        def get__authors(self):
            return self.authors