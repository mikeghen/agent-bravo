from web3 import Web3
from eth_account import Account
import os

PROPOSAL_ID = 15224123984213267098960411943118752395520351317670802264568797987915327925042
GOVERNOR_ADDRESS = "0x9c5D85d2A24C2059C46950548c937f0a392849Ce"

# ABI snippet for the delegate contract's publishOpinionAndVote function
DELEGATE_ABI = [{
    "inputs": [
        {"name": "proposalId", "type": "uint256"},
        {"name": "support", "type": "uint8"},
        {"name": "opinion", "type": "string"},
        {"name": "reasoning", "type": "string"}
    ],
    "name": "publishOpinionAndVote",
    "outputs": [{"name": "voteWeight", "type": "uint256"}],
    "stateMutability": "nonpayable",
    "type": "function"
}]

PROPOSAL_CREATED_EVENT_ABI = {
    "anonymous": False,
    "inputs": [
        {"indexed": False, "internalType": "uint256", "name": "proposalId", "type": "uint256"},
        {"indexed": False, "internalType": "address", "name": "proposer", "type": "address"},
        {"indexed": False, "internalType": "address[]", "name": "targets", "type": "address[]"},
        {"indexed": False, "internalType": "uint256[]", "name": "values", "type": "uint256[]"},
        {"indexed": False, "internalType": "string[]", "name": "signatures", "type": "string[]"},
        {"indexed": False, "internalType": "bytes[]", "name": "calldatas", "type": "bytes[]"},
        {"indexed": False, "internalType": "uint256", "name": "voteStart", "type": "uint256"},
        {"indexed": False, "internalType": "uint256", "name": "voteEnd", "type": "uint256"},
        {"indexed": False, "internalType": "string", "name": "description", "type": "string"}
    ],
    "name": "ProposalCreated",
    "type": "event"
}

GOVERNOR_ABI_SNIPPET = [{
    "inputs": [{"name": "proposalId", "type": "uint256"}],
    "name": "state",
    "outputs": [{"name": "", "type": "uint8"}],
    "stateMutability": "view",
    "type": "function"
}]

def publish_opinion_and_vote(gov_decision, proposal_id=PROPOSAL_ID):
    """
    Publishes the opinion and vote to the blockchain using the delegate contract.
    
    Args:
        gov_decision: GovDecision object containing opinion, reasoning, and vote
    
    Returns:
        transaction receipt
    """
    # Get required environment variables
    rpc_url = os.getenv('RPC_URL')
    private_key = os.getenv('PRIVATE_KEY')
    delegate_address = os.getenv('DELEGATE_ADDRESS')
    
    if not rpc_url:
        raise ValueError("RPC_URL environment variable is not set")
    if not private_key:
        raise ValueError("PRIVATE_KEY environment variable is not set")
    if not delegate_address:
        raise ValueError("DELEGATE_ADDRESS environment variable is not set")
        
    # Set up Web3 connection
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    
    # Set up account from private key
    account = Account.from_key(private_key)
    
    # Create contract instance
    delegate_contract = w3.eth.contract(
        address=delegate_address,
        abi=DELEGATE_ABI
    )
    
    # Prepare transaction
    transaction = delegate_contract.functions.publishOpinionAndVote(
        proposal_id,
        gov_decision.vote,
        gov_decision.opinion,
        gov_decision.reasoning
    ).build_transaction({
        'from': account.address,
        'nonce': w3.eth.get_transaction_count(account.address),
        'gasPrice': w3.eth.gas_price
    })
    
    # Sign and send transaction
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    
    # Wait for transaction receipt
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Transaction successful! Hash: {tx_hash.hex()}")
    return tx_receipt 


def get_proposal_created_events(from_block=122220603, to_block="latest"):
    """
    Subscribes to the AgentBravoGovernor contract and retrieves ProposalCreated events.
    Gets logs in chunks of 50,000 blocks to avoid RPC limits.
    
    Args:
        from_block (int): The block number to start searching for events (default is 0).
        to_block (int or str): The block number to end the search (default is "latest").
    
    Returns:
        List: A list of ProposalCreated event logs.
    """
    # Get the RPC_URL environment variable
    rpc_url = os.getenv('RPC_URL')
    if not rpc_url:
        raise ValueError("RPC_URL environment variable is not set")
    
    # Set up the Web3 connection
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    
    # Convert 'latest' to actual block number if needed
    if to_block == "latest":
        to_block = w3.eth.block_number
    
    # Create contract instance
    governor_address = "0x9c5D85d2A24C2059C46950548c937f0a392849Ce"
    governor_abi = [PROPOSAL_CREATED_EVENT_ABI]
    governor_contract = w3.eth.contract(address=governor_address, abi=governor_abi)
    
    # Initialize variables
    chunk_size = 50000
    all_logs = []
    current_from_block = from_block
    
    # Get logs in chunks
    while current_from_block <= to_block:
        # Calculate the end block for this chunk
        current_to_block = min(current_from_block + chunk_size - 1, to_block)
        
        # Get logs for the current chunk
        logs = governor_contract.events.ProposalCreated().get_logs(
            from_block=current_from_block,
            to_block=current_to_block
        )
        all_logs.extend(logs)
        
        # Move to the next chunk
        current_from_block = current_to_block + 1


        
        print(f"Processed blocks {current_from_block-chunk_size} to {current_to_block}")

    # Clean logs to only include proposalId and description
    cleaned_logs = []
    for log in all_logs:
        cleaned_log = {
            'proposalId': log.args.proposalId,
            'description': log.args.description
        }
        cleaned_logs.append(cleaned_log)
    
    all_logs = cleaned_logs

    return all_logs 

def has_voted(proposal_id, voter_address):
    """
    Checks if an address has already voted on a specific proposal.
    
    Args:
        proposal_id (int): The ID of the proposal to check
        voter_address (str): The address to check for voting history
        
    Returns:
        bool: True if the address has voted, False otherwise
    """
    # Get the RPC_URL environment variable
    rpc_url = os.getenv('RPC_URL')
    if not rpc_url:
        raise ValueError("RPC_URL environment variable is not set")
    
    # Set up Web3 connection
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    
    # Create contract instance
    governor_contract = w3.eth.contract(
        address=GOVERNOR_ADDRESS,
        abi=GOVERNOR_ABI_SNIPPET
    )
    
    # Check if address has voted
    try:
        has_voted = governor_contract.functions.hasVoted(proposal_id, voter_address).call()
        return has_voted
    except Exception as e:
        print(f"Error checking vote status: {e}")
        return False


def get_proposal_status(proposal_id):
    """
    Gets the status of a proposal from the Governor contract.
    
    Args:
        proposal_id (int): The ID of the proposal
    
    Returns:
        str: Status of the proposal ('pending', 'active', 'canceled', 'defeated', 
             'succeeded', 'queued', 'expired', 'executed')
    """
    # Get the RPC_URL environment variable
    rpc_url = os.getenv('RPC_URL')
    if not rpc_url:
        raise ValueError("RPC_URL environment variable is not set")
    
    # Set up Web3 connection
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    
    # Create contract instance
    governor_contract = w3.eth.contract(
        address=GOVERNOR_ADDRESS,
        abi=GOVERNOR_ABI_SNIPPET
    )
    
    # Get the proposal state
    state_number = governor_contract.functions.state(proposal_id).call()
    
    # Map state number to string
    states = {
        0: 'pending',
        1: 'active',
        2: 'canceled',
        3: 'defeated',
        4: 'succeeded',
        5: 'queued',
        6: 'expired',
        7: 'executed'
    }
    
    return states.get(state_number, 'unknown') 