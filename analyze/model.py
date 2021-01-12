
from abc import ABC, abstractmethod

class Model(ABC):

    @classmethod
    def build_model(cls, name):
        if(name == 'useless'):
            return UselessModel()

    @abstractmethod
    def insert_and_decide(self, email, txt):
        pass

    @abstractmethod
    def list_to_label(self):
        pass

    @abstractmethod
    def process_labels(self, lbls):
        pass

class UselessModel(Model):

    def __init__(self):
        pass

    def insert_and_decide(self, email, txt):
        return False

    def list_to_label(self):
        return ['https://www.google.com', 'http://mudhaniu.x10host.com', 'https://stackoverflow.com']

    def process_labels(self, lbls):
        print(lbls)