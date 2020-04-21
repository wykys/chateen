#!/usr/bin/env python3
# wykys 2020
# knihovna pro práci s korpusem

from database import *

inactive = [p for p in db.get_participants() if p.get_cnt_messages() < 50]
print(inactive)


inactive = [c for c in db.get_chats() if c.get_cnt_messages() < 100]


for c in inactive:
    p = c.participants
    print(p)
