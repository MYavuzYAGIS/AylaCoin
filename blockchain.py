import datetime
import hashlib
import json

from flask import Flask, jsonify, request


# Part 1 - Building a Blockchain
class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(proof=1, previous_hash='0')  # genesis block and proof =1 is the proof of work. 1 is arbitrary number.








# Part 2 - Mining our Blockchain
