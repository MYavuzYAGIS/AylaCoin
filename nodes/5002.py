import datetime
import hashlib
import json
import uuid
from http.client import HTTPResponse
from sys import implementation
from urllib.parse import urlparse
from uuid import uuid4

import requests
from flask import Flask, jsonify, request


class aylaCoin:
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.create_block(proof=1, previous_hash="0")
        self.nodes = set()  # set is cheaper on the ram compared to list.

    def create_block(self, proof, previous_hash):
        block = {
            "index": len(self.chain) + 1,
            "timestamp": str(datetime.datetime.now()),
            "proof": proof,
            "previous_hash": previous_hash,
            "transactions": self.transactions,
        }
        self.transactions = (
            []
        )  # after adding the transactions to the block, I need to empty the list so no repetition in the block registry.
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(
                str(new_proof**2 - previous_proof**2 - 2**10).encode()
            ).hexdigest()
            if hash_operation[:5] == "00000":
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            current_block = chain[block_index]
            if current_block["previous_hash"] != self.hash(previous_block):
                return False
            previous_proof = previous_block["proof"]
            current_proof = current_block["proof"]
            hash_operation = hashlib.sha256(
                str(current_proof**2 - previous_proof**2 - 2**10).encode()
            ).hexdigest()
            if hash_operation[:5] != 00000:
                False
            previous_block = current_block
            block_index += 1
        return True

    def add_transaction(self, sender, receiver, amount):
        self.transactions.append(
            {"sender": sender, "receiver": receiver, "amount": amount}
        )
        previous_block = self.get_previous_block()
        return (
            previous_block["index"] + 1
        )  # last block is aleady finished working. Hence, i need the one after the last one.

    def add_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response = requests.get(f"http://{node}/get_chain/")
            if response.status_code == 200:
                length = response.json()["length"]
                chain = response.json()["chain"]
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
            return True
        return False


# ====== implementation =======
aylacoin = aylaCoin()

# Create an address for the node on port 5000
node_address = str(uuid4()).replace("-", "")


app = Flask(__name__)


@app.route("/mine_block", methods=["GET"])
def mine_block():
    if request.method != "GET":
        return "Wrong HTTP VERB!"
    previous_block = aylacoin.get_previous_block()
    previous_proof = previous_block["proof"]
    previous_hash = aylacoin.hash(previous_block)
    aylacoin.add_transaction(sender=node_address, receiver='Kyoto',amount=100)
    proof = aylacoin.proof_of_work(previous_proof)
    block = aylacoin.create_block(
        proof, previous_hash
    )  # create_block returns a block
    response = {
        "message": "Congrats! you mined a block11!!!111",
        "index": block["index"],
        "timestamp": block["timestamp"],
        "proof": block["proof"],
        "previous_hash": block["previous_hash"],
        "transactions": block["transactions"],
    }
    return jsonify(response), 200


@app.route("/get_chain", methods=["GET"])
def get_chain():
    if request.method != "GET":
        return "Wrong HTTP VERB!"
    response = {"chain": aylacoin.chain, "length": len(aylacoin.chain)}
    return jsonify(response), 200


# check whether if the blockchain is valid
@app.route("/validate", methods=["GET"])
def validate():
    chain = aylacoin.chain
    result = aylacoin.is_chain_valid(chain)
    if result:
        response = " This is a valid Chain"
    else:
        response = "Not  a Valid chain"
    return response, 200


@app.route("/add_transaction",methods=["POST"])
def add_transaction():
    json = request.get_json()
    transaction_keys = ['sender','receiver','amount']
    if not all(key in json for key in transaction_keys):
        return 'Missing information. Please provice Sender, Receiver, and Amount in request body', 400
    index = aylacoin.add_transaction(json['sender'],json['receiver'],json['amount'])
    response = {
        'message' : f'Transaction is added to the block: {index}'
    }
    return jsonify(response), 201

@app.route("/connect_node",methods=["POST"])
def connect_node():
    json = request.get_json()
    nodes = json.get('nodes') # addresses
    if nodes is None:
        return "Empty Node List", 401 
    for node in nodes:
        aylacoin.add_node(node)
    response = {
        "message": "Nodes are connected in the network.",
        "total_nodes": list(aylacoin.nodes)
    }
    return jsonify(response),201


@app.route("/replace_chain", methods=["GET"])
def replace_chain():
    is_chain_replaced = aylacoin.replace_chain()
    if is_chain_replaced:
        response = {
            "message": "Chain was replaced with the longest one.",
            "new_chain": aylacoin.chain
        }
    else:
        response = {
            "message":"nothing to replace. it is already the longest one.",
            "current_chain": aylacoin.chain
        }
    return jsonify(response), 200
    






app.run(host="0.0.0.0", port=5002)
