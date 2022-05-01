import os
from tinkoff.invest import Client

TOKEN_READ = os.environ["TOKEN_READ"]


def main():
    with Client(TOKEN_READ) as client:
        print(client.users.get_accounts())



if __name__ == "__main__":
    main()

