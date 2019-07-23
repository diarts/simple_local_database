class Database:
    """simple local RAM database"""

    def __init__(self):
        self.main_storage = {}
        self.cash_of_storages = []
        self.transaction_deep = False
        self.command_dict = {'set': self.set,
                             'get': self.get,
                             'unset': self.unset,
                             'counts': self.counts,
                             'begin': self.start_transaction,
                             'commit': self.commit_transition,
                             'rollback': self.roll_back,
                             'help': self.help,
                             'end': self.end}
        print('Database started')

    def set(self, data: list):
        if len(data) < 2:
            return
        elif len(data) % 2 != 0:
            print('Error! For one of enter variables does not exist value')
            return

        for i in range(0, len(data), 2):
            name = data[i]
            value = data[i + 1]

            if self.transaction_deep:
                self.cash_of_storages[-1][name] = value
            else:
                self.main_storage[name] = value

    def get(self, data: list):
        for variable in data:
            if self.transaction_deep:
                print(self.cash_of_storages[-1].get(variable) or 'NULL')
            else:
                print(self.main_storage.get(variable) or 'NULL')

    def unset(self, data: list):
        if self.transaction_deep:
            self.cash_of_storages[-1].pop(data[0], None) or print(f"Variable {data[0]} doesn't exist in database")
        else:
            self.main_storage.pop(data[0], None) or print(f"Variable {data[0]} doesn't exist in database")

    def counts(self, data: list):
        if data:
            if self.transaction_deep:
                counts = sum(value == data[0] for _, value in self.cash_of_storages[-1].items())
            else:
                counts = sum(value == data[0] for _, value in self.main_storage.items())
            print(counts)

    def start_transaction(self, *args):
        if self.transaction_deep:
            self.cash_of_storages.append(self.cash_of_storages[-1].copy())
        else:
            self.cash_of_storages.append(self.main_storage.copy())
            self.transaction_deep = True

    def commit_transition(self, *args):
        if not self.cash_of_storages:
            print('Error! This command worked only in transaction context')
        elif len(self.cash_of_storages) > 1:
            self.cash_of_storages[-1] = self.cash_of_storages.pop(-1)
        else:
            self.main_storage = self.cash_of_storages.pop(-1)
            self.transaction_deep = False

    def roll_back(self, *args):
        if not self.cash_of_storages:
            print('Error! This command worked only in transaction context')
        elif len(self.cash_of_storages) > 1:
            self.cash_of_storages.pop(-1)
        else:
            self.cash_of_storages.pop(-1)
            self.transaction_deep = False

    def help(self, *args):
        print(
            """This commands work whith this database:
            SET <variable> <value> - add new <variable> with <value> in database. Couple of variable and it value can 
                                     be infinity count;
            GET <variable>         - return from database value for <variable> or NULL if variable does not exist;
            UNSET <variable>       - delete <variable> from database;
            COUNTS <value>         - return count of variable with <value> if database
            
            BEGIN                  - start transaction (before you enter command commit, every change in transaction 
                                     don't affect at database and occure in copy of database)
            COMMIT                 - confirm the transaction changes and transfered it to database
            ROLLBACK               - roll back all transaction changes
            END                    - exit application and delete database
            """)

    def end(self, *args):
        print('Database closed')
        exit(0)

    def wait_command(self):
        """Main database work loop"""

        while True:
            try:
                raw = input('-> ').strip()
            except EOFError:
                self.end()
            else:

                if not raw:
                    continue
                else:
                    data = raw.split(' ')
                    command = data[0].lower()

                    if self.command_dict.get(command):
                        self.command_dict.get(command)(data[1:])
                    else:
                        print(f'Error! command {command} is not found. You can enter "help" if you need command list')


if __name__ == '__main__':
    a = Database()
    a.wait_command()
