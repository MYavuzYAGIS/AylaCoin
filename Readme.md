# WIP


An experimental blockchain creation, mining, verification excersize.

Also on top of that is build `AylaCoin` where `decentralized` nodes in the network can exchange `AylaCoin` with each other.

# blockchain.py 

## Dependencies
Flask
requests

## App URL

`http://0.0.0.0:5000/${endpoint}`

## endpoints:
-> `/mine_block`
<br/>
-> `get_chain`
<br/>
-> `validate`


## Functionalities:

### mine_block

When a request is made to the endpoint '/mine_block', the node creates a new block and adds it to the chain. Minings is expected to be completed once the first 5 digits of the `hashlib.sha256(str(current_proof**2-previous_proof**2 - 2**10).encode()).hexdigest()` function are equal to '00000`.


### get_chain

When a request is made to the endpoint '/get_chain', the node returns the entire chain and also the length of the chain. If no mining is made before the request, the chain will only show the `genesis` block.


## validate

using the validate endpoint, the node will check if the chain is valid or not.






# AylaCoin.py 


<p> Basically an experimental custom cryptocurrency based on the blockchain.py implementation above. </p>

</br>

AylaCoin

</br>


## endpoints:
-> `/add_transaction`  ==> POST request
<br/>

<br/>

