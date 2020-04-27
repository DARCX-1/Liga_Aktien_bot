import json

KEY_SYMBOL = 'symbol'

class Watchlist:
    def __init__(self, file):
        self.file = file
        self.data = {}

    def length(self):
        return len(self.data)

    def add(self, item):
        self.data.append(item)

    def del(self, item):
        # avoid errors
        # search item
        # delete item
        return 0

    def load(self):
        with open(self.file) as json_file:
            data = json.load(json_file)
        return data

    def save(self):
        with open(file, 'w') as outfile:
            json.dump(data, outfile)
