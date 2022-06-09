[![CodeFactor](https://www.codefactor.io/repository/github/myavuzyagis/aylacoin/badge)](https://www.codefactor.io/repository/github/myavuzyagis/aylacoin) [![Codacy Badge](https://app.codacy.com/project/badge/Grade/893675d30e8a42e3a3847fa84c4e71b6)](https://www.codacy.com/gh/MYavuzYAGIS/AylaCoin/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=MYavuzYAGIS/AylaCoin&amp;utm_campaign=Badge_Grade)

![logo](screenshots/logo.png)

# MVP

An experimental blockchain creation, mining, verification excersize.

Also on top of that is build `AylaCoin` where `decentralized` nodes in the network can exchange `AylaCoin` with each other.

### Mock Data

in the mock/*.json files, you can find the mock data for the nodes and the transaction format.

# blockchain.py

This is the core blockchain logic where the AylaCoin is based on.

## Dependencies

Flask
requests

## App URL

`http://0.0.0.0:5000/${endpoint}`

## endpoints

-> `/mine_block`
<br/>
-> `get_chain`
<br/>
-> `validate`

## Functionalities

### mine_block

When a request is made to the endpoint '/mine_block', the node creates a new block and adds it to the chain. Minings is expected to be completed once the first 5 digits of the `hashlib.sha256(str(current_proof**2-previous_proof**2 - 2**10).encode()).hexdigest()` function are equal to '00000`.

![add_transaction](screenshots/mine_block.png)

### get_chain

When a request is made to the endpoint '/get_chain', the node returns the entire chain and also the length of the chain. If no mining is made before the request, the chain will only show the `genesis` block.

![add_transaction](screenshots/get_chain.png)

## validate

using the validate endpoint, the node will check if the chain is valid or not.

![add_transaction](screenshots/validate.png)

# AylaCoin.py

<p> Basically an experimental custom cryptocurrency based on the blockchain.py implementation above. </p>

## endpoints

-> `/add_transaction`  ==> POST request
</br>
given the parameters `sender` and `recipient` and `amount`, the node will create a new transaction and add it to the list of transactions.

![add_transaction](screenshots/add_transaction.png)

</br>

-> `/connect_node`  ==> POST request

![add_transaction](screenshots/connect_node.png)

</br>
Takes the nodes from a JSON file (mock data is used), checks whether the json file actually contains any adresses.
If there is at least one address, the node will connect to the node and add it to the list of nodes hence forming a network.

</br>

-> `/replace_chain`  ==> GET request

replaces the chain with the longest chain in the network.

<h2>Finalized Transaction Screenshot</h2>

</br>

<h4> beware the sender and receiver which shows that the nodes are connected, the consensus is established and transactions are successfully made</h4>

</br>

![add_transaction](screenshots/transaction_receipt.png)
