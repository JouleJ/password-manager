import pathlib
import getpass

from store import read_items, write_items, Item
from generate import generate_password
from crypto import encrypt_data, decrypt_data, compute_sha256

from .commands import Command


HOME = pathlib.Path('~').expanduser()
MIN_LEN_MASTERPASSWORD = 8

CMDS = []
HELP = Command(name='HELP', code='h', description='Show help').add_to_list(CMDS)
QUIT = Command(name='QUIT', code='q', description='Exit this CLI').add_to_list(CMDS)
READ = Command(name='READ', code='r', description='Load from disk to RAM, overriding whatever is in the latter').add_to_list(CMDS)
WRITE = Command(name='WRITE', code='w', description='Store to the disk (overriding). Be careful').add_to_list(CMDS) 
ADD  = Command(name='ADD', code='a', description='Add new entry to RAM').add_to_list(CMDS)
SHOW = Command(name='SHOW', code='s', description='Show all entries in RAM').add_to_list(CMDS)

def help():
    print('COMMAND\tCODE\tDESCRIPTION')
    for cmd in CMDS:
        print('{}\t{}\t{}'.format(cmd.name, cmd.code, cmd.description))


def pretty_print_items(items):
    for idx, item in enumerate(items):
        print('Item {}'.format(idx + 1))

        if item.website_url:
            print('Website: {}'.format(item.website_url))

        if item.login:
            print('Login: {}'.format(item.login))

        print('Password: {}'.format(item.password))
        print()


def main():
    fpath = HOME / 'password_table.bin'
    items = []

    while True:
        words = input().strip().rstrip().split()
        if not words:
            continue

        if words[0] == QUIT.code and len(words) == 1:
            break
        elif words[0] == HELP.code and len(words) == 1:
            help()
        elif words[0] == READ.code and len(words) == 1:
            masterpassword = getpass.getpass('Enter masterpassword:')
            if len(masterpassword) < MIN_LEN_MASTERPASSWORD:
                print('Masterpassword cannot be so short')
                continue

            key = compute_sha256(masterpassword)
            del masterpassword

            cyphertext = None
            with fpath.open('rb') as fhandle:
                cyphertext = fhandle.read()
            lines = decrypt_data(cyphertext, key)
            items = read_items(lines)
            del lines
        elif words[0] == WRITE.code and len(words) == 1:
            masterpassword = getpass.getpass('Enter masterpassword:')
            if len(masterpassword) < MIN_LEN_MASTERPASSWORD:
                print('Masterpassword cannot be so short')
                continue

            key = compute_sha256(masterpassword)
            del masterpassword

            plaintext = write_items(items)
            cyphertext = encrypt_data(plaintext, key)
            del plaintext

            with fpath.open('wb') as fhandle:
                fhandle.write(cyphertext)
                del cyphertext
        elif words[0] == ADD.code and len(words) == 1:
            login = input('Enter login (leave empty for none):')
            website_url = input('Enter website url (leave empty for none):')
            password = input('Enter password (leave empty for autogenerate):')
            if not password:
                password = generate_password()

            items.append(Item(login=login, website_url=website_url, password=password))
        elif words[0] == SHOW.code and len(words) == 1:
            pretty_print_items(items)
        else:
            raise RuntimeError('Unknown command: {}'.format(' '.join(words)))


if __name__ == '__main__':
    main()
