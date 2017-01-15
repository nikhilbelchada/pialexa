import pickle


class Credential(object):
    def __init__(self):
        try:
            with open('cred.pkl', 'rb') as cred_file:
                self.data = pickle.load(cred_file)
        except IOError:
            self.data = {}

    def dump(self, updated_data):
        self.data.update(updated_data)

        with open('cred.pkl', 'wb') as cred_file:
            pickle.dump(self.data, cred_file)