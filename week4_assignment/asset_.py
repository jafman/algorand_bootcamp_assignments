from algosdk.v2client import algod
from algosdk.future.transaction import AssetConfigTxn, wait_for_confirmation
from algosdk.mnemonic import to_private_key
from algosdk.future import transaction

algod_address = "https://testnet-api.algonode.cloud"
algod_client = algod.AlgodClient("", algod_address)
asset_creator_address = "525DFKTVFYJ376DI6KY27ERBMPCFXGAU63VETLOJAN7ZK5MXDRJCHN7UWQ"
passphrase = "oblige accuse obtain solve setup capable section love hurry buddy charge neck wrist panel group clinic maximum concert smooth cube coach project talk absent gadget"
assetId = None
sender_private_key = to_private_key(passphrase)

txn = AssetConfigTxn(
    sender=asset_creator_address,
    sp=algod_client.suggested_params(),
    total=50000,
    default_frozen=False,
    unit_name="ENB",
    asset_name="enb",
    manager=asset_creator_address,
    reserve=asset_creator_address,
    freeze=asset_creator_address,
    clawback=asset_creator_address,
    url="https://www.google.com",
    decimals=0)

signed_txn = txn.sign(sender_private_key)

#send xtn to network and get txn id
try:
    txid = algod_client.send_transaction(signed_txn)
    print("Signed transaction with TXID: {}".format(txid))
    confirmed_txn = wait_for_confirmation(algod_client, txid, 4)
    print("Txn ID: {}".format(txid))
    print("Result confirmed in round: {}".format(confirmed_txn["confirmed-round"]))
except Exception as err:
    print(err)

transaction_response = algod_client.pending_transaction_info(txid)
assetId = transaction_response["asset-index"]
print("Asset-id:", assetId)




# ---------------------------------------------------------------------------------------------
# OPT IN
# ---------------------------------------------------------------------------------------------

params = algod_client.suggested_params()
optin_account = "W5DDEKLYHTEX6QMFHEUL7VDA6ZUZMRLMG6XWR73ZAYTGQORNEVPIGD4JFU"
passphrase = "border risk lucky boil drill memory avocado aware ceiling outside machine steel foster bulk lend voice coin spread few stage taxi rain model able section"
private_key = to_private_key(passphrase)
account_info = algod_client.account_info(optin_account)
holding = None
idx = 0
for my_account_info in account_info['assets']:
    scrutinized_asset = account_info['assets'][idx]
    idx = idx + 1    
    if (scrutinized_asset['asset-id'] == assetId):
        holding = True
        break
if not holding:
    # Use the AssetTransferTxn class to transfer assets and opt-in
    txn = transaction.AssetTransferTxn(
        sender=optin_account,
        sp=params,
        receiver=optin_account,
        amt=0,
        index=assetId)
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

receiving_account = "W5DDEKLYHTEX6QMFHEUL7VDA6ZUZMRLMG6XWR73ZAYTGQORNEVPIGD4JFU"
params = algod_client.suggested_params()
txn = transaction.AssetTransferTxn(
    sender=asset_creator_address,
    sp=params,
    receiver=receiving_account,
    amt=2000,
    index=assetId)
signed_txn = txn.sign(sender_private_key)
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