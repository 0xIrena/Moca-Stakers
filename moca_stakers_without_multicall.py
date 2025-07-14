import os
import json
from dotenv import load_dotenv
from web3 import Web3
from web3.exceptions import ContractLogicError
from datetime import datetime
import time

# Load environment variables from .env file
load_dotenv()

# Configuration
RPC_URL = os.getenv("RPC_URL")
CONTRACT_ADDRESS = "0x9a98E6B60784634AE273F2FB84519C7F1885AeD2"  # MOCA Staking Contract Address
ADDRESS = os.getenv("ADDRESS")
CONTRACT_ABI = json.loads('''
[{"inputs":[{"internalType":"address","name":"mocaToken","type":"address"},{"internalType":"uint256","name":"startTime_","type":"uint256"},{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"updater","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[{"internalType":"address","name":"target","type":"address"}],"name":"AddressEmptyCode","type":"error"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"AddressInsufficientBalance","type":"error"},{"inputs":[],"name":"EnforcedPause","type":"error"},{"inputs":[],"name":"ExpectedPause","type":"error"},{"inputs":[],"name":"FailedInnerCall","type":"error"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"OwnableInvalidOwner","type":"error"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"OwnableUnauthorizedAccount","type":"error"},{"inputs":[{"internalType":"address","name":"token","type":"address"}],"name":"SafeERC20FailedOperation","type":"error"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferStarted","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"account","type":"address"}],"name":"Paused","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Staked","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address[]","name":"users","type":"address[]"},{"indexed":true,"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"name":"StakedBehalf","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"account","type":"address"}],"name":"Unpaused","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Unstaked","type":"event"},{"inputs":[],"name":"acceptOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newUpdater","type":"address"}],"name":"changeUpdater","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"getMocaToken","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getPoolCumulativeWeight","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getPoolLastUpdateTimestamp","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getStartTime","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getTotalCumulativeWeight","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getTotalStaked","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getUpdater","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"getUser","outputs":[{"components":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"cumulativeWeight","type":"uint256"},{"internalType":"uint256","name":"lastUpdateTimestamp","type":"uint256"}],"internalType":"struct SimpleStaking.Data","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"getUserCumulativeWeight","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"pause","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"paused","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"pendingOwner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"stake","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address[]","name":"users","type":"address[]"},{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"name":"stakeBehalf","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"unpause","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"unstake","outputs":[],"stateMutability":"nonpayable","type":"function"}]
''')

# ERC20 ABI to query token decimals and name
ERC20_ABI = [
    {
        "inputs": [],
        "name": "decimals",
        "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "name",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function"
    }
]

# Initialize Web3
w3 = Web3(Web3.HTTPProvider(RPC_URL))
print(f"Connected: {w3.is_connected()}")
print(f"Chain ID: {w3.eth.chain_id}")
print(f"Current Date/Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Initialize staking contract
contract = w3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=CONTRACT_ABI)

# Initialize variables with default values to prevent NameError
moca_token = None
token_name = "MOCA"  # Default to MOCA based on contract
decimals = 18  # Default to 18 if token query fails
total_staked = 0.0 # Default to 0.0
is_paused = False # Default to False

# Query staked token address
try:
    moca_token = contract.functions.getMocaToken().call()
    print(f"Staked Token Address: {moca_token}")
except Exception as e:
    print(f"getMocaToken error: {e}")
    # moca_token remains None

# Query token name and decimals
if moca_token:
    token_contract = w3.eth.contract(address=Web3.to_checksum_address(moca_token), abi=ERC20_ABI)
    try:
        token_name = token_contract.functions.name().call()
        print(f"Token Name: {token_name}")
    except Exception as e:
        print(f"Token name error: {e}")
    try:
        decimals = token_contract.functions.decimals().call()
        print(f"Token Decimals: {decimals}")
    except Exception as e:
        print(f"Token decimals error: {e}")

# Query total staked amount
try:
    total_staked = contract.functions.getTotalStaked().call() / (10**decimals)
    print(f"Total Staked (All Users): {total_staked:,.2f} {token_name}")
except Exception as e:
    print(f"getTotalStaked error: {e}")
    # total_staked remains 0.0

# Verify paused status
try:
    is_paused = contract.functions.paused().call()
    print(f"Contract Paused: {is_paused}")
except Exception as e:
    print(f"paused error: {e}")
    # is_paused remains False

# Load staker addresses from previous run if available
stakers_file = "staker_addresses.json"
stakers = {}
if os.path.exists(stakers_file):
    with open(stakers_file, "r") as f:
        staker_list = json.load(f)
        stakers = {addr: 0 for addr in staker_list}
    print(f"Loaded {len(stakers)} staker addresses from {stakers_file}")
else:
    # Fetch all stakers
    block_step = 1000000
    start_block = 20280000  # Approximate block for July 2024
    end_block = w3.eth.block_number
    print(f"Fetching Staked and StakedBehalf events from block {start_block} to {end_block}")

    # Process Staked events
    for block in range(start_block, end_block + 1, block_step):
        try:
            events = contract.events.Staked().get_logs(
                from_block=block,
                to_block=min(block + block_step - 1, end_block),
                argument_filters={}
            )
            for event in events:
                user = event['args']['user']
                if Web3.is_address(user) and user not in stakers:
                    stakers[user] = 0
            print(f"Processed Staked events for block range [{block}, {min(block + block_step - 1, end_block)}]: {len(events)} events")
        except Exception as e:
            print(f"Error fetching Staked events in block range [{block}, {min(block + block_step - 1, end_block)}]: {e}")

    # Process StakedBehalf events
    for block in range(start_block, end_block + 1, block_step):
        try:
            events = contract.events.StakedBehalf().get_logs(
                from_block=block,
                to_block=min(block + block_step - 1, end_block),
                argument_filters={}
            )
            for event in events:
                users = event['args']['users']
                for user in users:
                    if Web3.is_address(user) and user not in stakers:
                        stakers[user] = 0
            print(f"Processed StakedBehalf events for block range [{block}, {min(block + block_step - 1, end_block)}]: {len(events)} events")
        except Exception as e:
            print(f"Error fetching StakedBehalf events in block range [{block}, {min(block + block_step - 1, end_block)}]: {e}")

    # Save only valid staker addresses
    valid_stakers = [addr for addr in stakers.keys() if Web3.is_address(addr)]
    with open(stakers_file, "w") as f:
        json.dump(valid_stakers, f)
    print(f"Saved {len(valid_stakers)} staker addresses to {stakers_file}")

# Load existing balances if available
balances_file = "staker_balances.json"
if os.path.exists(balances_file):
    with open(balances_file, "r") as f:
        stakers = json.load(f)
    print(f"Loaded {len(stakers)} staker balances from {balances_file}")

# Query balances with rate limit handling
print(f"Found {len(stakers)} unique stakers. Querying balances...")
if not os.path.exists(balances_file):
    for i, user in enumerate(list(stakers.keys()), 1):
        if stakers[user] != 0:  # Skip already processed balances
            continue
        retries = 3
        backoff = 1
        while retries > 0:
            try:
                user_data = contract.functions.getUser(user).call()
                stakers[user] = user_data[0] / (10 ** decimals)  # Convert to human-readable
                break
            except ContractLogicError as e:
                print(f"getUser revert for {user}: {e}")
                stakers[user] = 0
                break
            except Exception as e:
                if "429" in str(e) or "Too Many Requests" in str(e):
                    print(f"429 error for {user}. Retrying in {backoff}s...")
                    time.sleep(backoff)
                    backoff *= 2  # Exponential backoff
                    retries -= 1
                else:
                    print(f"getUser error for {user}: {e}")
                    stakers[user] = 0
                    break
        if i % 100 == 0:  # Print progress every 100 stakers
            print(f"Processed {i}/{len(stakers)} staker balances")
            # Save partial balances
            with open(balances_file, "w") as f:
                json.dump(stakers, f)
            print(f"Saved partial balances to {balances_file}")

# Save final balances
with open(balances_file, "w") as f:
    json.dump(stakers, f)
print(f"Saved staker balances to {balances_file}")

# Sort stakers by balance (descending)
sorted_stakers = sorted(stakers.items(), key=lambda x: x[1], reverse=True)

# Filter for stakers with positive balance
stakers_with_positive_balance = [
    (address, balance) for address, balance in sorted_stakers if balance > 0
]


# Save to file
output_file = "moca_stakers_top_list.txt"
with open(output_file, 'w') as f:
    token_name = token_name.upper()
    f.write(f"${token_name} Stakers Top List\n")
    f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"Contract Address: {CONTRACT_ADDRESS}\n")
    f.write(f"Token Name: ${token_name}\n")
    f.write(f"Total Staked: {total_staked:,.2f} ${token_name}\n")
    f.write(f"Contract Paused: {is_paused}\n")
    f.write(f"Total Stakers: {len(stakers_with_positive_balance)}\n")
    f.write("\nRank | Wallet Address | Staked Balance (${token_name})\n".format(token_name=token_name))
    f.write("-" * 60 + "\n")
    for i, (address, balance) in enumerate(sorted_stakers, 1):
        if balance > 0:  # Only include non-zero balances
            f.write(f"{i} | {address} | {balance:,.2f} ${token_name}\n")

print(f"Top stakers list saved to {output_file}")