import datetime
import hashlib
import json
import uuid
from http.client import HTTPResponse
from urllib.parse import urlparse
from uuid import uuid4

import requests
from flask import Flask, jsonify, request


class Blockchain:
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.create_block(proof=1, previous_hash='0')  

    def create_block(self,proof,previous_hash):
        block = {
            'index' : len(self.chain) + 1, 
            'timestamp' : str(datetime.datetime.now()), 
            'proof' : proof, 
            'previous_hash' : previous_hash,
            'transactions' : self.transactions 
        }
        self.transactions = []  # after adding the transactions to the block, I need to empty the list so no repetition in the block registry. 
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1] 
    

    def proof_of_work(self, previous_proof):
        new_proof = 1 
        check_proof = False 
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2-previous_proof**2 - 2**10).encode()).hexdigest() 
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
    def add_transaction(self, sender, receiver, amount):
        self.transactions.append({
            "sender" : sender,
            "receiver" : receiver,
            "amount" : amount
            })
        previous_block = self.get_previous_block()
        return previous_block['index'] + 1 # last block is aleady finished working. Hence, i need the one after the last one.
blockchain = Blockchain()

app = Flask(__name__)

@app.route('/mine_block',methods=["GET"])
def mine_block():
    if request.method != "GET":
        return "Wrong HTTP VERB!"
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    previous_hash = blockchain.hash(previous_block)
    proof =blockchain.proof_of_work(previous_proof)
    block = blockchain.create_block(proof,previous_hash) # create_block returns a block
    response = {
        'message':"Congrats! you mined a block11!!!111",
        'index':block['index'],
        'timestamp':block['timestamp'],
        'proof': block['proof'],
        'previous_hash':block['previous_hash']
        }
    return jsonify(response), 200



@app.route('/get_chain',methods=["GET"])
def get_chain():
    if request.method != "GET":
        return "Wrong HTTP VERB!"
    response = {
        'chain':blockchain.chain,
        'length':len(blockchain.chain) 
    }
    return jsonify(response), 200    



# check whether if the blockchain is valid

@app.route('/validate',methods=["GET"])
def validate():
    chain = blockchain.chain
    result = blockchain.is_chain_valid(chain)
    if result:
        response = " This is a valid Chain"
    else:
        response = "Not  a Valid chain"
    return response,200
    


app.run(host='0.0.0.0',port=5000)
