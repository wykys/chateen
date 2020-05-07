#!/usr/bin/env python3

from chateen import db
from chateen import Loader


if __name__ == '__main__':
    Loader('../data/bug_message_1.json')
    db.reduce()