import datetime
import hashlib
import json

from flask import Flask, jsonify, request


# Part 1 - Building a Blockchain
class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(proof=1, previous_hash='0')  # genesis block and proof =1 is the proof of work. 1 is arbitrary number.

    def create_block(self,proof,previous_hash):
        block = {
            'index' : len(self.chain) + 1,  # index is the number of blocks in the chain.
            'timestamp' : str(datetime.datetime.now()), # timestamp is the time of the block creation.
            'proof' : proof, # proof is the proof of work.
            'previous_hash' : previous_hash # previous_hash is the hash of the previous block.
        }
        self.chain.append(block)
        return block






# Part 2 - Mining our Blockchain
