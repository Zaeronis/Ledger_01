import sqlite3 as sql
from ledger import *

class User:
    def __init__(self):
        pass

    def create_uid(self):
        conn, c = l.open_ledger()
        while True:
            uid = ''.join(r.choices(st.ascii_letters + st.digits, k=16))
            condition = re.search(r'(?=.*[A-Z])(?=.*[a-z])(?=.*\d)', uid)
            if condition is None:
                print('UID invalid')
                print('Trying again...')
                pass
            elif uid in c.execute(f'SELECT uid FROM ledger_users').fetchall():
                print('UID already exists')
                print('Trying again...')
                pass
            else:
                break
        l.close_ledger(conn, c)
        return uid

    def get_uid(self, uname):
        conn, c = l.open_ledger()
        c.execute(f'SELECT uid FROM ledger_users WHERE username = "{uname}"')
        uid = c.fetchone()[0]
        l.close_ledger(conn, c)
        return uid

    def create_username(self):
        conn, c = l.open_ledger()
        while True:
            uname = input('Please enter a username:\n')
            conditions = not re.fullmatch(r'((?=.*[a-z])|(?=.*[A-Z]))[A-Za-z0-9_!~@#]{3,16}', uname)
            if conditions:
                print('''
                \nUsername must be between 3 and 16 character, 
                contain at least one or more letters or numbers,
                and the following characters:   _   @   #   !   ~''')
                pass
            else:
                break
        return uname

    def create_name(self, pos):
        while True:
            name = input(f'Please enter your {pos} name: ')
            condition = not re.fullmatch(r'[A-Za-z]+', name)
            if condition:
                print('Name can only contain only letters.\n')
                pass
            else:
                break
        return name

    def create_password(self):
        while True:
            password = input('Please enter a password:\n')
            conditions = not re.fullmatch(r'(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,32}', password)
            if conditions:
                print('''Password must be at least
                 8 - 32 characters long, have at least
                 one capital and lowercase letter
                 each, one number, and one
                 special character.\n''')
                pass
            else:
                password = ph.hash(password)
                confirmation = input('Please confirm your password:\n')
                try:
                    if ph.verify(password, confirmation):
                        print("Success! Password saved.")
                except:
                    print("Passwords do not match. Please try again.")
                    continue
                break
        return password

    def validate_password(self, uname, psswd):
        conn, c = l.open_ledger()
        uid = self.get_uid(uname)
        password = c.execute(f'SELECT password FROM user_passwords WHERE uid = "{uid}"').fetchone()[0]
        try:
            ph.verify(password, psswd)
            l.close_ledger(conn, c)
            return True
        except:
            l.close_ledger(conn, c)
            return False

    def update_password(self, uname):
        conn, c = l.open_ledger()
        uid = self.get_uid(uname)
        psswd = input('Please enter your current password: ')
        if not self.validate_password(uname, psswd):
            print('Invalid password.')
            l.close_ledger(conn, c)
            return None
        else:
            print('Password is valid.')
            print('Updating password...')
            password = self.create_password()
            c.execute(f'UPDATE user_passwords SET password = "{password}" WHERE uid = "{uid}"')
            conn.commit()
            l.close_ledger(conn, c)
            return password

    def create_user(self):
        conn, c = l.open_ledger()
        condition = 'True' in c.execute(f'SELECT logged_in FROM ledger_users').fetchall()
        if condition:
            print('Please log out before creating a new user.')
            return None
        else:
            uid = self.create_uid()
            username = self.create_username()
            first_name = self.create_name('first')
            last_name = self.create_name('last')
            password = self.create_password()
            logged_in = 'True'
            datetime = str(dt.datetime.now())
            c.execute(f'INSERT INTO ledger_users VALUES (?,?,?,?,?,?)', (uid, username, first_name, last_name, logged_in, datetime))
            c.execute(f'INSERT INTO user_passwords VALUES (?,?,?)', (uid, password, datetime))
            conn.commit()
            l.close_ledger(conn, c)
        return uid, username, first_name, last_name, password

    def user_login(self, username, password):
        conn, c = l.open_ledger()
        condition = 'True' in c.execute(f'SELECT logged_in FROM ledger_users').fetchall()
        if condition:
            print('You are already logged in. Please log out to log into an account.')
            return None
        else:
            if self.validate_password(username, password):
                c.execute(f'UPDATE ledger_users SET logged_in = "True" WHERE uid = "{self.get_uid(username)}"')
                conn.commit()
                l.close_ledger(conn, c)
                print('Login successful.')
                return True
            else:
                print('Invalid username or password.')
                l.close_ledger(conn, c)
                return False

    def user_logout(self, username):
        conn, c = l.open_ledger()
        condition = 'True' not in c.execute(f'SELECT logged_in FROM ledger_users WHERE username = "{username}"').fetchone()
        if condition:
            print('You are not logged in.')
            l.close_ledger(conn, c)
            return None
        else:
            print('Logging out...')
            c.execute(f'UPDATE ledger_users SET logged_in = "False" WHERE username = "{username}"')
            conn.commit()
            l.close_ledger(conn, c)
            return True

u = User()