class Database:
    """simple local RAM database"""
    MAIN_STORAGE = {}
    CASH_STORAGE = {}

    def __init__(self):
        self.is_transaction = False
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

        for i in range(0, len(data), 2):
            name = data[i]
            value = data[i + 1]

            if self.is_transaction:
                self.CASH_STORAGE[name] = value
            else:
                self.MAIN_STORAGE[name] = value
                self.roll_back()

    def get(self, data: list):
        for variable in data:
            if self.is_transaction:
                print(self.CASH_STORAGE.get(variable) or 'NULL')
            else:
                print(self.MAIN_STORAGE.get(variable) or 'NULL')

    def unset(self, data: list):
        if self.is_transaction:
            self.CASH_STORAGE.pop(data[0], None) or print(f"Variable {data[0]} doesn't exist in database")
        else:
            self.MAIN_STORAGE.pop(data[0], None) or print(f"Variable {data[0]} doesn't exist in database")
            self.roll_back()

    def counts(self, data: list):
        if data:
            if self.is_transaction:
                counts = sum(value == data[0] for _, value in self.CASH_STORAGE.items())
            else:
                counts = sum(value == data[0] for _, value in self.MAIN_STORAGE.items())
            print(counts)

    def start_transaction(self, *args):
        self.is_transaction = True

    def commit_transition(self, *args):
        self.MAIN_STORAGE = self.CASH_STORAGE.copy()
        self.is_transaction = False

    def roll_back(self, *args):
        self.CASH_STORAGE = self.MAIN_STORAGE.copy()
        self.is_transaction = False

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
