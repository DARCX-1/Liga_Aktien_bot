import json

KEY_SYMBOL = 'symbol'
KEY_CHAT = 'chat'
KEY_ID = 'id'
KEY_PRICE = 'price'

# fragen, wie bekomme ich es hin, dass ich jetzt noch das stehen habe dass vorne die chat id steht und hinten die symbole?
# wie speichere ich die Keys bei json.dump als int


class Watchlist:

    def __init__(self, file):
        self.file = file
        self.data = {}

    def length(self):
        return len(self.data)

    def add(self, item, chat):
        # if chat in self.data.keys():
            # self.data[chat][KEY_SYMBOL].append(item)
        # else:
        #     temp_dict = {}
        #     item_list = []
        #     item_list.append(item)
        #     temp_dict[KEY_SYMBOL] = item_list
        #     self.data[chat] = temp_dict
        # return self.data

        if chat in self.data.keys():
            temp_dict = {}
            temp_dict[KEY_SYMBOL] = item
            temp_dict[KEY_PRICE] = 5
            self.data[chat].append(temp_dict)
        else:
            values = []
            temp_dict = {}
            temp_dict[KEY_SYMBOL] = item
            temp_dict[KEY_PRICE] = 5
            values.append(temp_dict)
            self.data[chat] = values
        return self.data

    def delete(self, item, chat):
        try:
            for v in self.data[chat]:
                if v[KEY_SYMBOL] == item:
                    self.data[chat].remove(v)
        except Exception as e:
            print(e)
        return self.data

    def load(self):
        with open(self.file) as json_file:
            data = json.load(json_file, object_hook=lambda d: {int(
                k) if k.lstrip('-').isdigit() else k: v for k, v in d.items()})
        return data

    def save(self, data):
        with open(self.file, 'w') as outfile:
            json.dump(data, outfile, ensure_ascii=True)
# class DBHelper:

#     def __init__(self, dbname="Watchlist.sqlite"):
#         dbname = dbname
#         self.conn = sqlite3.connect(dbname)

#     def setup(self):
#         tblstmt = "CREATE TABLE IF NOT EXISTS items (description text, owner text)"
#         itemidx = "CREATE INDEX IF NOT EXISTS itemIndex ON items (description ASC)"
#         ownidx = "CREATE INDEX IF NOT EXISTS ownIndex ON items (owner ASC)"
#         self.conn.execute(tblstmt)
#         self.conn.execute(itemidx)
#         self.conn.execute(ownidx)
#         self.conn.commit()

#     def add_item(self, item_text, owner):
#         stmt = "INSERT INTO items (description, owner) VALUES (?, ?)"
#         args = (item_text, owner)
#         self.conn.execute(stmt, args)
#         self.conn.commit()

#     def delete_item(self, item_text, owner):
#         stmt = "DELETE FROM items WHERE description = (?) AND owner = (?)"
#         args = (item_text, owner)
#         self.conn.execute(stmt, args)
#         self.conn.commit()

#     def get_items(self, owner):
#         stmt = "SELECT description FROM items WHERE owner= (?)"
#         args = (owner,)
        # return [x[0] for x in self.conn.execute(stmt, args)]
