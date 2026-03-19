import typer, getpass 
from utils.encrypt import encrypt_file, decrypt_file
from utils.database import create_db_and_tables, engine
from utils.models import Secrets
from sqlmodel import Session
from sqlalchemy.exc import IntegrityError
from rich import print

# Example usage
db_file = 'utils/mybase.db'
app = typer.Typer()

# Encrypt the database file
#encrypt_file(db_file, password)

# Decrypt to access the database
#decrypt_file(db_file, password)

# You can now use sqlite3 normally
#conn = sqlite3.connect(db_file)
# Perform your database operations...


def get_pass() -> (str, str, bool):
    pwd = getpass.getpass("Enter a new password >>> ")
    conf = getpass.getpass("Verify your password >>> ")
    dl = pwd == conf
    return pwd, dl

def login() -> bool:
    pwd = getpass.getpass("Enter your password >>> ")
    try:
        decrypt_file(db_file, pwd)
    except Exception as e:
        print(e)
        return pwd, False
    return pwd, True

@app.command()
def init() -> None:
    '''
    Create a database for your keys and encrypt them with your password.
    '''
    print("Initializing the database...")
    while True:
        pwd, dl = get_pass()
        if dl:
            create_db_and_tables()
            encrypt_file(db_file, pwd)
            print("Database created successfully.")
            break
        else:
            print("Wrong password. Try again.")

@app.command()
def add() -> None:
    '''
    Add a key to your database.
    '''
    while True:
        pwd, dl = login()
        if dl:
            key = input("API Key >>> ")
            name = input("Key Name >>> ")
            project = input("Project Name >>> ")
            expiration_date = input("Expiration Date (MM-DD-YYYY) >>> ")
            with Session(engine) as session:
                try:
                    new_key = Secrets(key=key,
                                      name=name,
                                      project=project,
                                      expiration_date=expiration_date)
                    session.add(new_key)
                    session.commit()
                except IntegrityError:
                    session.rollback()
                    encrypt_file(db_file, pwd)
                    print("Key already exists.")
                    break
                else:
                    encrypt_file(db_file, pwd)
                    print("Key added successfully.")
                    break
        else:
            print("Wrong password. Try again.")

if __name__ == "__main__":
    app()

