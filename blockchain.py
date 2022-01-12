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
        
        for block in chain:
            if block['previous_hash'] != previous_hash:
                return False
            
            proof = block['proof']
            hashed_proof = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            
            if hashed_proof[:4] != '0000':
                return False
            
            previous_hash = self.hash_block(block)
            previous_proof = proof
            
        return True
            
    def mine_block(self):
        pass


# Mining
        
bc = Blockchain()
print(bc.is_chain_valid(bc.chain))