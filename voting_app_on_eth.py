import json
import web3

from web3 import Web3, HTTPProvider, TestRPCProvider
from solc import compile_source
from web3.contract import ConciseContract
from binascii import hexlify
import codecs

contract_file = 'Voting.sol'
with open(contract_file, 'r') as myfile:
    code = myfile.read()

compiled_sol = compile_source(code)
contract_interface = compiled_sol['<stdin>:Voting']

#w3 = Web3(TestRPCProvider(port=8546))
w3 = Web3(TestRPCProvider())

# Instantiate and deploy contract
bytecode = contract_interface['bin']
contract = w3.eth.contract(abi=contract_interface['abi'], bytecode=bytecode)

# Get transaction hash from deployed contract
candidates = [b'Rama', b'Niki', b'Jose']
tx_hash = contract.deploy(args=[candidates], transaction={'from': w3.eth.accounts[0], 'gas': 410000}) 

# Get tx receipt to get contract address
tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
contract_address = tx_receipt['contractAddress']

# Contract instance in concise mode
abi = contract_interface['abi']
contract_instance = w3.eth.contract(address=contract_address, abi=abi, ContractFactoryClass=ConciseContract)

print('Validating the Rama candidate')
print(contract_instance.validCandidate('Rama'))
print('Validating fake candidates are not allowed')
print(contract_instance.validCandidate('Fake'))
print('Total votes for Rama')
print(contract_instance.totalVotesFor('Rama'))
print('Add 1 vote for Rama')
contract_instance.voteForCandidate('Rama', transact={})
print('Total votes for Rama')
print(contract_instance.totalVotesFor('Rama'))
