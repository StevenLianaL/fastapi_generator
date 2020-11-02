from abc import abstractmethod


class App:
    def create_app(self):
        self.write_files()

    @abstractmethod
    def write_files(self):
        """"""
