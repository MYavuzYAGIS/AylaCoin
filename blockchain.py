import datetime
import hashlib
import json
from http.client import HTTPResponse

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
            'previous_hash' : previous_hash, # previous_hash is the hash of the previous block.

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

# Mining Blockchain

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

# get full blockchain.

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
