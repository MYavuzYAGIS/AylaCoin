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

    def get_previous_block(self):
        return self.chain[-1] # returns the last block in the chain.

    def proof_of_work(self, previous_proof):
        new_proof = 1 # increment will need in each iteration until getting the right proof
        check_proof = False 
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2-previous_proof**2 - 2**10).encode()).hexdigest() # adding b' in the head.
            if hash_operation[:5] == '00000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self,chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            current_block = chain[block_index]
            if current_block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            current_proof = current_block['proof']
            hash_operation = hashlib.sha256(str(current_proof**2-previous_proof**2 - 2**10).encode()).hexdigest()
            if hash_operation[:5] != 00000:
                False    
            previous_block = current_block
            block_index += 1
        return True



# Part 2 - Mining our Blockchain

