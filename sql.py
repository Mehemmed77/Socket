import sqlite3

def insert_or_login_person(name: str,password: str) -> str:
    with sqlite3.connect('people.db') as sql:
        cr = sql.cursor()
        code_select = f"SELECT name FROM People WHERE name='{name.lower()}' and password='{password}'"

        cr.execute(code_select)
        data = cr.fetchall()

        if data:
            return f"\nUser Named {name.title()} Logged In."

        else:
            try:
                code = f"INSERT INTO People (name,password) values ('{name.lower()}','{password.lower()}')"
                cr.execute(code)
                return f"\nNew User Named {name.title()} Signed Up."
            
            except:
                print('Name Already Exists')

                exists = True

                while exists:
                    name = ''

                    while len(name)<3:
                        name = input('Your Name Again: ')
                    
                    code_select = f"SELECT name FROM People WHERE name='{name.lower()}'"
                    cr.execute(code_select)
                    exists = cr.fetchall()

                code = f"INSERT INTO People (name,password) values ('{name.lower()}','{password.lower()}')"
                cr.execute(code)

                return f"\nNew User Named {name.title()} Signed Up.",name
                    

