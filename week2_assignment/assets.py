import json
from algosdk.v2client import algod
from algosdk.future import transaction
from algosdk.mnemonic import to_private_key

algod_address = "https://testnet-api.algonode.cloud"
algod_client = algod.AlgodClient("", algod_address)
asset_creator_address = "525DFKTVFYJ376DI6KY27ERBMPCFXGAU63VETLOJAN7ZK5MXDRJCHN7UWQ"
passphrase = "oblige accuse obtain solve setup capable section love hurry buddy charge neck wrist panel group clinic maximum concert smooth cube coach project talk absent gadget"

private_key = to_private_key(passphrase)

# ---------------------------------------------------------------------------------------------
# CREATE AN ASSET
# ---------------------------------------------------------------------------------------------
txn = transaction.AssetConfigTxn(
    sender=asset_creator_address,
    sp=algod_client.suggested_params(),
    total=1000,
    default_frozen=False,
    unit_name="JAF",
    asset_name="jafar",
    manager=asset_creator_address,
    reserve=asset_creator_address,
    freeze=asset_creator_address,
    clawback=asset_creator_address,
    url="https://www.google.com",
    decimals=0)

signed_txn = txn.sign(private_key)

#send xtn to network and get txn id
try:
    txid = algod_client.send_transaction(signed_txn)
    print("Signed transaction with TXID: {}".format(txid))
    confirmed_txn = transaction.wait_for_confirmation(algod_client, txid, 4)
    print("Txn ID: {}".format(txid))
    print("Result confirmed in round: {}".format(confirmed_txn["confirmed-round"]))
except Exception as err:
    print(err)

print("Transaction Information: {}".format(
        json.dumps(confirmed_txn, indent=4)))

# ---------------------------------------------------------------------------------------------
# MODIFY AN ASSET (Update Manager)
# ---------------------------------------------------------------------------------------------

new_manager_account = "U3V575NMHL2BJRYITNZ7UAZNPLRJC3EPOWQUPHCP3ONOA277EAAKNMLAN4"
asset_index = 149430547
params = algod_client.suggested_params()
txn = transaction.AssetConfigTxn(
    sender=asset_creator_address,
    sp=params,
    index=asset_index, 
    manager=new_manager_account,
    reserve=asset_creator_address,
    freeze=asset_creator_address,
    clawback=asset_creator_address)

signed_txn = txn.sign(private_key)

#send xtn to network and get txn id
try:
    txid = algod_client.send_transaction(signed_txn)
    print("Signed transaction with TXID: {}".format(txid))
    confirmed_txn = transaction.wait_for_confirmation(algod_client, txid, 4)
    print("Txn ID: {}".format(txid))
    print("Result confirmed in round: {}".format(confirmed_txn["confirmed-round"]))
except Exception as err:
    print(err)

print("Transaction Information: {}".format(
        json.dumps(confirmed_txn, indent=4)))

# ---------------------------------------------------------------------------------------------
# OPT IN
# ---------------------------------------------------------------------------------------------

params = algod_client.suggested_params()
current_account = "U3V575NMHL2BJRYITNZ7UAZNPLRJC3EPOWQUPHCP3ONOA277EAAKNMLAN4"
passphrase = "oblige accuse obtain solve setup capable section love hurry buddy charge neck wrist panel group clinic maximum concert smooth cube coach project talk absent gadget"
private_key = to_private_key(passphrase)
asset_id= 149430547
account_info = algod_client.account_info(current_account)
holding = None
idx = 0
for my_account_info in account_info['assets']:
    scrutinized_asset = account_info['assets'][idx]
    idx = idx + 1    
    if (scrutinized_asset['asset-id'] == asset_id):
        holding = True
        break
if not holding:
    # Use the AssetTransferTxn class to transfer assets and opt-in
    txn = transaction.AssetTransferTxn(
        sender=current_account,
        sp=params,
        receiver=current_account,
        amt=0,
        index=asset_id)
    signed_txn = txn.sign(private_key)
    # Send the transaction to the network and retrieve the txid.
    try:
        txid = algod_client.send_transaction(signed_txn)
        print("Signed transaction with txID: {}".format(txid))
        # Wait for the transaction to be confirmed
        confirmed_txn = transaction.wait_for_confirmation(algod_client, txid, 4) 
        print("TXID: ", txid)
        print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))    
    except Exception as err:
        print(err)

# ---------------------------------------------------------------------------------------------
# TRANSFER ASSET
# ---------------------------------------------------------------------------------------------
receiving_account = "U3V575NMHL2BJRYITNZ7UAZNPLRJC3EPOWQUPHCP3ONOA277EAAKNMLAN4"
asset_id= 149430547
passphrase = "oblige accuse obtain solve setup capable section love hurry buddy charge neck wrist panel group clinic maximum concert smooth cube coach project talk absent gadget"
private_key = to_private_key(passphrase)
params = algod_client.suggested_params()
txn = transaction.AssetTransferTxn(
    sender=asset_creator_address,
    sp=params,
    receiver=receiving_account,
    amt=10,
    index=asset_id)
signed_txn = txn.sign(private_key)
# Send the transaction to the network and retrieve the txid.
try:
    txid = algod_client.send_transaction(signed_txn)
    print("Signed transaction with txID: {}".format(txid))
    # Wait for the transaction to be confirmed
    confirmed_txn = transaction.wait_for_confirmation(algod_client, txid, 4) 
    print("TXID: ", txid)
    print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))
except Exception as err:
    print(err)

# ---------------------------------------------------------------------------------------------
# FREEZE ASSET
# ---------------------------------------------------------------------------------------------
params = algod_client.suggested_params()

account_to_freeze = "U3V575NMHL2BJRYITNZ7UAZNPLRJC3EPOWQUPHCP3ONOA277EAAKNMLAN4"

txn = transaction.AssetFreezeTxn(
    sender=asset_creator_address,
    sp=params,
    index=asset_id,
    target=account_to_freeze,
    new_freeze_state=True   
    )
signed_txn = txn.sign(private_key)
# Send the transaction to the network and retrieve the txid.
try:
    txid = algod_client.send_transaction(signed_txn)
    print("Signed transaction with txID: {}".format(txid))
    # Wait for the transaction to be confirmed
    confirmed_txn = transaction.wait_for_confirmation(algod_client, txid, 4)  
    print("TXID: ", txid)
    print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))    
except Exception as err:
    print(err)

# ---------------------------------------------------------------------------------------------
# REVOKE ASSET
# ---------------------------------------------------------------------------------------------
params = algod_client.suggested_params()
account_to_revoke = "U3V575NMHL2BJRYITNZ7UAZNPLRJC3EPOWQUPHCP3ONOA277EAAKNMLAN4"
txn = transaction.AssetTransferTxn(
    sender=asset_creator_address,
    sp=params,
    receiver=asset_creator_address,
    amt=10,
    index=asset_id,
    revocation_target=account_to_revoke
    )
signed_txn = txn.sign(private_key)
# Send the transaction to the network and retrieve the txid.
try:
    txid = algod_client.send_transaction(signed_txn)
    print("Signed transaction with txID: {}".format(txid))
    # Wait for the transaction to be confirmed
    confirmed_txn = transaction.wait_for_confirmation(algod_client, txid, 4)
    print("TXID: ", txid)
    print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))      
except Exception as err:
    print(err)