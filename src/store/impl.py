from dataclasses import dataclass
from typing import List
import base64


BEGIN_ITEM = 'begin_item'
END_ITEM = 'end_item'
PASSWORD = 'password'
LOGIN = 'login'
WEBSITE = 'website'


@dataclass
class Item:
    website_url: str
    login: str
    password: str


def b64encode(s):
    return base64.standard_b64encode(s.encode('utf-8')).decode('utf-8')


def b64decode(s):
    return base64.standard_b64decode(s).decode('utf-8')


def write_items(items: List[Item]) -> List[str]:
    lines = []

    for item in items:
        lines.append(BEGIN_ITEM)

        if item.website_url:
            encoded_value = b64encode(item.website_url)
            lines.append('{} {}'.format(WEBSITE, encoded_value))

        if item.login:
            encoded_value = b64encode(item.login)
            lines.append('{} {}'.format(LOGIN, encoded_value))

        if item.password:
            encoded_value = b64encode(item.password)
            lines.append('{} {}\n'.format(PASSWORD, encoded_value))

        lines.append(END_ITEM + '\n')

    return lines


def read_items(lines: List[str]) -> List[Item]:
    items = []
    current_item = None

    for line in lines:
        words = line.strip().rstrip().split()
        if words:
            if words[0] == BEGIN_ITEM and len(words) == 1:
                if current_item is None:
                    current_item = Item(website_url='', login='', password='')
                else:
                    raise RuntimeError('Bad sequence: superflous {} command, cannot load password table'.format(words[0]))
            elif words[0] == END_ITEM and len(words) == 1:
                if current_item is None:
                    raise RuntimeError('Bad sequence: superflous {} commmand, cannot load password table'.format(words[0]))
                else:
                    items.append(current_item)
                    current_item = None
            elif words[0] == PASSWORD and len(words) == 2:
                if current_item is None:
                    raise RuntimeError('Bad sequence: superflous {} commmand, cannot load password table'.format(words[0]))
                else:
                    current_item.password = b64decode(words[1])
            elif words[0] == LOGIN and len(words) == 2:
                if current_item is None:
                    raise RuntimeError('Bad sequence: superflous {} commmand, cannot load password table'.format(words[0]))
                else:
                    current_item.login =b64decode(words[1])
            elif words[0] == WEBSITE and len(words) == 2:
                if current_item is None:
                    raise RuntimeError('Bad sequence: superflous {} commmand, cannot load password table'.format(words[0]))
                else:
                    current_item.website_url = b64decode(words[1])
            else:
                raise RuntimeError('Bad sequence: unknown command, cannot load password table')

    if current_item is not None:
        raise RuntimeError('Bad sequence: missing {} command, cannot load password'.format(END_ITEM))

    return items
