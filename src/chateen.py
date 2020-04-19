#!/usr/bin/env python3
# Chateen program pro vytváření korpusové databáze
# ze sociálních sítí
# wykys 2020

from fb_loader import FbLoader


if __name__ == '__main__':
    loader = FbLoader()
    loader.save()

