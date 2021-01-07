
import os
import pickle

class BulkDocProcessor:

    def _read_file(self, file_path):
        f = open(file_path, 'rb')
        data = pickle.load(f)
        f.close()
        return data

    def _next_file(self):
        self.doc_iter = self._read_file(self.file_iter.__next__().path).__iter__()

    def __init__(self):
        self.file_iter = os.scandir('../../../../data/docs').__iter__()
        self.doc_iter = None

        self.file_ctr = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return self.doc_iter.__next__()
        except:
            self._next_file()
            return self.doc_iter.__next__()