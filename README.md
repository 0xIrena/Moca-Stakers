# List of top $MOCA stakers

I couldn't find a list of the top $MOCA stakers (or at least not an accurate one), so I decided to make one myself.

This script writes 3 files:
- staker_addresses.json
- staker_balances.json
- moca_stakers_top_list.txt

When you want to configure a new list, you should delete both of the .json files. Due to the fact that multicall hasn't been implemented, the script is quite slow (processing each address individually).

You need your own [Infura API key](https://developer.metamask.io/) to use this script.

## .env
```
RPC_URL="https://mainnet.infura.io/v3/YOUR_KEY"
CONTRACT_ADDRESS="0x9a98E6B60784634AE273F2FB84519C7F1885AeD2"
```

## Example output
An example output has been included in the files (`moca_stakers_top_list.txt`).

## Note
This list might miss some addresses that have received an airdrop, but never (un)staked any tokens. This script only fetches the addresses that have interacted with the staking contract.