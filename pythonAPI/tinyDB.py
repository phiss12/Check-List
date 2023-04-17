from tinydb import TinyDB

class tinyDB:
    
    def __init__(self, fileName):
        self.db = TinyDB(fileName)
    
    def insert(self, stuff, date, due):
        self.db.insert({"Todo": stuff, "Timestamp": date, "Deadline": due})
    
    def update(self, dict, id):
        self.db.update(dict, doc_ids=[int(id)])
    
    def remove(self, id):
        self.db.remove(doc_ids=[int(id)])

    def all(self):
        return self.db.all()
