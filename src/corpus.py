# wykys 2020
# knihovna pro práci s korpusem

class Corpus(object):
    def __init__(self, author: str):
        self.author = author
        self.messages = []

    def add(self, item: str):
        self.messages.append(f'<s>{item}</s>\n')

    def save(self):
        with open(f'../out/{self.author}.txt', 'w', encoding='utf-8') as fw:
            fw.writelines(self.messages)
