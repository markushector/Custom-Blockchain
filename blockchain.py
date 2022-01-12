#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 11 23:19:52 2022

@author: markushector
"""

import datetime
import hashlib
import json
from flask import Flask, jsonify


# Blockchain

class Blockchain():
    
    def __init__(self):
        self.chain = []
        self.create_block(proof=1, previous_hash='0')
        
    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain) + 1,
                 'timestamp': datetime.datetime.now(),
                 'proof': proof,
                 'previous_hash': previous_hash
                 }
        
        self.chain.append(block)
        return block
    
    def get_previous_block(self):
        return self.chain[-1]
    
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while not check_proof:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    def hash_block(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
        
    def is_chain_valid(self, chain):
        
        previous_hash = '0'
        previous_proof = 1
        
        for i, block in enumerate(chain):
            if i == 0:
                previous_hash = self.hash_block(block)
                previous_proof = proof
                continue
            
            if block['previous_hash'] != previous_hash:
                return False
            
            proof = block['proof']
            hashed_proof = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            
            if hashed_proof[:4] != '0000':
                return False
            
            previous_hash = self.hash_block(block)
            previous_proof = proof
            
        return True
            

# Creating a webapp       
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
        
# Creating a blockchain
bc = Blockchain()

# Mining
@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = bc.get_previous_block()
    previous_proof = previous_block['proof']
    proof = bc.proof_of_work(previous_proof)
    previous_hash = bc.hash_block(previous_block)
    block = bc.create_block(proof, previous_hash)
    response = {'message': 'Glhf',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']}
    return jsonify(response), 200

@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {'chain': bc.chain,
                'length': len(bc.chain)}
    return jsonify(response), 200

app.run(host='0.0.0.0', port=5000)
    
