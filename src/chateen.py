#!/usr/bin/env python3
# Chateen program pro vytváření korpusové databáze
# ze sociálních sítí
# wykys 2020

from loader_fb import FbLoader


if __name__ == '__main__':
    loader = FbLoader()
    loader.save()

