import queue
from . import stack
import time


class Parser:

    def __init__(self, text, *args, **kwargs):
        self.tokens = []
        self._parser = self.Parser(text)
        self._bytesparser = self.BytesParser(text)
        self.processText = "".join(text.decode().split()) + "$"
        self.stack = stack.Stack()
        self.queue = queue.Queue()
        self.separator = ["+", ":", " ", ",", "$"]

    @property
    def parser(self):
        return self._parser

    @property
    def bytesparser(self):
        return self._bytesparser

    def tokenizer(self):
        for letter in self.processText:
            notin = False
            token = []
            if letter in self.separator:
                notin = True
        #         print(i ,x,notin)
                self.stack.push(letter)
                while not self.queue.empty():
                    token.append(self.queue.get())
                tokenString = "".join(token)
                if tokenString:
                    self.tokens.append("".join(token))
            if not notin:
                self.queue.put(letter)
        return self.tokens

    def Parser(self, text):
        text = text.replace(b"\r", b"")
        text = "".join(text.decode().split("\n")[2:])
        text = "".join(text.split("OK")[0])
        return(text)

    def BytesParser(self, text):
        text = text.replace(b"\r", b"")
        text = b"".join(text.split(b"\n")[2:])
        text = text.split(b"OK")[0]
        return text
