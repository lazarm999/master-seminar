from algosdk import account, mnemonic
from algosdk import transaction, v2client
from algosdk.v2client.algod import AlgodClient
from algosdk.mnemonic import from_private_key
from algosdk import logic
from beaker import localnet
import algosdk
import json
from pyteal import *
import base64
import pystache 
import time

token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
server = "http://localhost:4001"

# token = ''
# server = 'https://testnet-api.algonode.cloud'
client = AlgodClient(token, server)

testnet_accounts = [
    {"private_key": "jWEec+IRsWuVfHu/fQxM1qSei/B4UvqEG1X8G/+SZDz1tfB92iXxvCmLtE5N7KIAMBVnEwhhwaolusmfZT5o1Q==", "address": "6W27A7O2EXY3YKMLWRHE33FCAAYBKZYTBBQ4DKRFXLEZ6ZJ6NDKXXQOAFQ"},
    {"private_key": "oCmfF2dY6OT4aea3rDvHiDZGr7T/qD5GBG8C1OCQiHpoWQJ3zP4Cvn00YwjmmNC1j4tp927I6cf/KLPNaDqVZQ==", "address": "NBMQE56M7YBL47JUMMEONGGQWWHYW2PXN3EOTR77FCZ422B2SVSSBVGJYU"},
    {"private_key": "WRGq8tBC7ghc9jSs9d71P+80GPSNkUdxmSu1ocYDvpyTrzdSosec1auBueMxuUie4h/4AoXMrXGEnDyAmMS7uA==", "address": "SOXTOUVCY6ONLK4BXHRTDOKIT3RB76ACQXGK24METQ6IBGGEXO4ICSGVVA"},
    {"private_key": "W7J3mtOjZoreIj/HPuPOg+cIKRqY1YqzLOXD/IqH4rqhAoUMPQaIfM5NWJ/qwYNsBz1yW8rqmxpr/8DwUzKcxw==", "address": "UEBIKDB5A2EHZTSNLCP6VQMDNQDT24S3ZLVJWGTL77APAUZSTTDX3TMGUQ"},
    {"private_key": "fzGnZvTBlWlINotb177ZcuLYAGCkCowuIoMTrO8M8Y0GME6yFJBva6qlKgZwylu1i7GimFiQsbu34lK2oPBB/Q==", "address": "AYYE5MQUSBXWXKVFFIDHBSS3WWF3DIUYLCILDO5X4JJLNIHQIH6WZ2WPZ4"},
    {"private_key": "Shp88028FNoIIa5SAIv2FH7dhRuXkZbMfqD+rGezhDjbZ2bRK2N7NJBWL/0IUXTvBarC9Ww+M4KJhvx+0limvg==", "address": "3NTWNUJLMN5TJECWF76QQULU54C2VQXVNQ7DHAUJQ36H5USYU27IOOFNXQ"},
    {"private_key": "/3DICaRyqsN6MnjS5vBi84IH4MWnFxclVgYSBJqvDWT+2KmQxKYhL3KTCqxt/xhT7u5xC4XftJcy4bqu3WhdGg==", "address": "73MKTEGEUYQS64UTBKWG37YYKPXO44ILQXP3JFZS4G5K5XLILUNORN35V4"},
    {"private_key": "HIFYpguMbwDY3budFZrTozju1rdeP+tLGr9e5zH1HgeF2p98UuiEieWPh8DN7OZMc1oDmK/CFeEzAx702nR84w==", "address": "QXNJ67CS5CCITZMPQ7AM33HGJRZVUA4YV7BBLYJTAMPPJWTUPTRV2SW6KQ"},
    {"private_key": "9/wrvdrs6r4BUzRgJWVLY20Wvl+sSoAKnjHUH+UMUC0Ql/xaAyV7rQlYtUA8mIOzYTL6+tU3muTIp3NDan4tZA==", "address": "CCL7YWQDEV522CKYWVADZGEDWNQTF6X22U3ZVZGIU5ZUG2T6FVSJVVKPMU"},
    {"private_key": "lS5i/AMG2So3mOLI8RCM/ki89Mb12sW9CZ2pBlpBJf14mm0XgZgwK2YsBAZarpMFELgH7ee2uemr+kr8n/SIbQ==", "address": "PCNG2F4BTAYCWZRMAQDFVLUTAUILQB7N463LT2NL7JFPZH7URBW44BGQEA"}
]

# created by account 0
testnet_app_ids = [
    731749744, 731749754, 731749755, 731749756, 731749766, 731749767, 731749768, 731749769,
    731749779, 731749780, 731749781, 731749782, 731749792, 731749793, 731749794, 731749795,
    731749796, 731749806, 731749807, 731749808, 731749818, 731749820, 731749821, 731749860,
    731749861, 731749878, 731749879, 731749881, 731749891, 731749892, 731749893, 731749894,
    731749905, 731749906, 731749907, 731749908, 731749909, 731749919, 731749920, 731749921,
    731749922, 731749933, 731749934, 731749935, 731749955, 731749956, 731749957, 731749958,
    731750001, 731750002, 731750004, 731750005, 731750006, 731750016, 731750017, 731750018,
    731750028, 731750029, 731750030, 731750031, 731750032, 731750042, 731750043, 731750044,
    731750045, 731750055, 731750056, 731750085, 731750103, 731750104, 731750105, 731750106,
    731750107, 731750117, 731750118, 731750119, 731750129, 731750130, 731750131
]
testnet_app_id = "731583360"

def get_wallet_accounts():
    return localnet.get_accounts()

first_account = get_wallet_accounts()[0]
second_account = get_wallet_accounts()[1]
third_account = get_wallet_accounts()[2]

def get_current_time_in_ms():
    return time.time_ns() // 1_000_000

def print_logs(logs):
    def decode_base64(encoded_string):
        return base64.b64decode(encoded_string).decode('utf-8')
    
    def decode_base64_int(encoded_int):
        return base64.b64decode(encoded_int)
    
    log_int = False
    for log in logs:
        try:
            # print(log)
            if log_int:
                print(int.from_bytes(decode_base64_int(log), byteorder="big"))
                log_int = False
            else:
                decoded = decode_base64(log)
                if decoded == "log_int":
                    log_int = True
                else:
                    print(decoded)
        except:
            print("Culdn't decode: " + log)

def modify_template_file(file_path, data, start="__", end="__"):
    # Read the template file
    with open(file_path, "r", encoding="utf-8") as f:
        template = f.read()
    
    # Prepend the custom delimiters directive
    # delimiter_directive = f"{{={{{start} {end}}}=}}"
    delimiter_directive = "{{=__ __=}}"
    template_with_delimiters = delimiter_directive + "\n" + template
    
    # Render the template with pystache
    rendered_content = pystache.render(template_with_delimiters, data)
    
    with open("/home/lazar/Documents/Seminar blockchain/contracts/algorand/pyteal/ProcessExecutionFinal.py", "w", encoding="utf-8") as f:
        f.write(rendered_content)

def extract_addresses(accounts, indexes=None):
    if indexes:
        return [accounts[i]["address"] for i in indexes if i < len(accounts)]
    return [account["address"] for account in accounts]

def create_account(include_print=False):
    new_account = account.generate_account()
    private_key, address = new_account

    # Convert the private key to a mnemonic for backup
    mnemonic_phrase = mnemonic.from_private_key(private_key)

    if include_print:
        print(f"Address: {address}")
        print(f"Private Key: {private_key}")
        print(f"Mnemonic Phrase: {mnemonic_phrase}")
    return {
        "address": address,
        "private_key": private_key
    }

def create_accounts(n, include_print=False):
    accounts = []
    for _ in range(n):
        accounts.append(create_account(include_print))
    return accounts

def fund_accounts(accounts):
    for i in range(len(accounts)):
        account = accounts[i]
        address = account["address"]
        funded_account = get_wallet_accounts()[0]
        
        # Fetch suggested transaction parameters
        params = client.suggested_params()

        # Create the payment transaction
        # amount = 592500-100000  # Amount in microAlgos
        # amount = 1000
        amount = 100000+1000
        txn = transaction.PaymentTxn(funded_account.address, params, address, amount)

        # Sign the transaction
        signed_txn = txn.sign(funded_account.private_key)

        # Send the transaction
        tx_id = client.send_transaction(signed_txn)
        transaction.wait_for_confirmation(client, tx_id, 2)

def print_accounts():
    for account in get_wallet_accounts():
        addr = account.address
        account_info = client.account_info(addr)
        balance = account_info.get('amount')
        print(f"Account balance {addr[:5]}...{addr[-5:]}: {balance:,.0f} microAlgos")

def payment_transaction(sender, receiver_address, amount):
    txn = transaction.PaymentTxn(
        sender=sender["address"],
        sp=client.suggested_params(),
        receiver=receiver_address,
        amt=amount
    )
    stxn = txn.sign(sender["private_key"])
    start_time = get_current_time_in_ms()
    tx_id = client.send_transaction(stxn)
    result = transaction.wait_for_confirmation(client, tx_id, 2)
    end_time = get_current_time_in_ms()
    return end_time-start_time
    # with open("output_" + str(sender["address"]) + ".json", "w") as json_file:
    #     json.dump(result, json_file, indent=4)

def compile_program(client, source_code):
    compile_response = client.compile(source_code)
    return base64.b64decode(compile_response['result'])
    # return bytes.fromhex(response["result"])

def initialize_tmp_contract(accounts = None, index=0, include_print=True):
    # Must be imported here because ProcessFinal.py gets changed through modify_template_file function
    # and we are left with stale version
    from TmpContract import approval_program, clear_program
    private_key = accounts[index]["private_key"]
    address = accounts[index]["address"]
    if include_print:
        print("-------------------------------------------------------------------")
    # wallet_accounts = get_wallet_accounts()
    txn = transaction.ApplicationCreateTxn(
        sender=address,
        sp=client.suggested_params(),
        on_complete=transaction.OnComplete.NoOpOC.real,
        approval_program=compile_program(client, compileTeal(approval_program(), mode=Mode.Application, version=6)),
        clear_program=compile_program(client, compileTeal(clear_program(), mode=Mode.Application, version=6)),
        global_schema=transaction.StateSchema(num_uints=0, num_byte_slices=1),
        local_schema=transaction.StateSchema(num_uints=0, num_byte_slices=0),
    )

    signed_txn = txn.sign(private_key)
    if include_print:
        print('initialize_contract signed')
    txid = client.send_transaction(signed_txn)
    if include_print:
        print('initialize_contract sent')
    response = transaction.wait_for_confirmation(client, signed_txn.get_txid())
    if include_print:
        print('initialize_contract confirmed')
        print(f"Created App with id: {response['application-index']}  in tx: {txid}")
        print("Response: ", response)
    return response['application-index']


def initialize_contract(accounts = None, index=0, include_print=True):
    # Must be imported here because ProcessFinal.py gets changed through modify_template_file function
    # and we are left with stale version
    from ProcessExecutionSimpleContract import approval_program, clear_program
    private_key = accounts[index]["private_key"]
    address = accounts[index]["address"]
    if include_print:
        print("-------------------------------------------------------------------")
    # wallet_accounts = get_wallet_accounts()
    txn = transaction.ApplicationCreateTxn(
        sender=address,
        sp=client.suggested_params(),
        on_complete=transaction.OnComplete.NoOpOC.real,
        approval_program=compile_program(client, compileTeal(approval_program(), mode=Mode.Application, version=6)),
        clear_program=compile_program(client, compileTeal(clear_program(), mode=Mode.Application, version=6)),
        global_schema=transaction.StateSchema(num_uints=5, num_byte_slices=5),
        local_schema=transaction.StateSchema(num_uints=0, num_byte_slices=0),
    )

    signed_txn = txn.sign(private_key)
    if include_print:
        print('initialize_contract signed')
    txid = client.send_transaction(signed_txn)
    if include_print:
        print('initialize_contract sent')
    response = transaction.wait_for_confirmation(client, signed_txn.get_txid())
    if include_print:
        print('initialize_contract confirmed')
        print(f"Created App with id: {response['application-index']}  in tx: {txid}")
        print("Response: ", response)
    return response['application-index']

def sign_and_send_transaction(txn, sender, include_print=True):
    signed_txn = txn.sign(sender["private_key"])
    if include_print:
        print('make_transaction signed')
    start_time = get_current_time_in_ms()
    tx_id = client.send_transaction(signed_txn)
    if include_print:
        print("Transaction id: ", tx_id)
        print('make_transaction sent')
    transaction.wait_for_confirmation(client, tx_id)
    elsapsed_time = calculate_elapsed_time(start_time, include_print)
    if include_print:
        print('make_transaction confirmed')
    tx_info = client.pending_transaction_info(tx_id)
    logs = tx_info.get('logs', [])
    if include_print:    
        print_logs(logs)
    return elsapsed_time

def reset_state(app_id, sender, include_print = True):
    params = client.suggested_params()
    txn = transaction.ApplicationCallTxn(
        sender=sender["address"],
        sp=params,
        index=app_id,
        on_complete=transaction.OnComplete.NoOpOC,
        app_args=[999],
    )
    return sign_and_send_transaction(txn, sender, include_print)

def change_state(app_id, sender, id, cond = 0, include_print = True):
    params = client.suggested_params()
    txn = transaction.ApplicationCallTxn(
        sender=sender["address"],
        sp=params,
        index=app_id,
        on_complete=transaction.OnComplete.NoOpOC,
        app_args=[id, cond],
    )
    
    return sign_and_send_transaction(txn, sender, include_print)

def execute_transaction(app_id, sender, args, accounts=None, include_print=True):
    print("args: ", args)
    txn = transaction.ApplicationCallTxn(
        sender=sender["address"],
        sp=client.suggested_params(),
        index=app_id,
        on_complete=transaction.OnComplete.NoOpOC,
        app_args=args,
        accounts=accounts
    )
    
    return sign_and_send_transaction(txn, sender, include_print)

def get_balance(account):
    return client.account_info(account['address'])['amount']

def calculate_total_balance(accounts):
    sum = 0
    for acc in accounts:
        sum += get_balance(acc)
    return sum

def print_accounts_balances(accounts):
    for acc in accounts:
        print(client.account_info(acc["address"])["amount"])

def create_contract():
    addresses = {}
    for i, a in enumerate(extract_addresses(testnet_accounts)):
        addresses["address" + str(i)] = a
    print(addresses)
    modify_template_file("/home/lazar/Documents/Seminar blockchain/contracts/algorand/pyteal/ProcessExecution.py", data=addresses)

def calculate_elapsed_time(start_time, include_print=True):
    # elapsed time is in seconds
    end_time = get_current_time_in_ms()
    elapsed_time = end_time - start_time
    if include_print:
        elapsed_time_in_seconds = elapsed_time // 1000
        minutes = int(elapsed_time_in_seconds // 60)
        seconds = elapsed_time_in_seconds % 60
        print(f"Elapsed time: {minutes} minutes and {seconds:.2f} seconds")
    return elapsed_time

def run_correct_test_simple_contract(accounts, app_id, include_print=True):
    participantsOrder = [0, 1, 2, 3, 4, 2, 2]
    sum = 0
    numTxn = 0
    elapsed_times = []
    for i, participantIndex in enumerate(participantsOrder):
        elapsed_time = change_state(app_id, accounts[participantIndex], id=i, include_print=include_print)
        elapsed_times.append(elapsed_time)
        sum += elapsed_time
        numTxn += 1
    return sum / numTxn

def run_correct_test_order_medication_contract(accounts, app_id, cond, app_address, to_distributor_amount=0, to_manufacturer_amount=0,  
        starting_step = 0, limit=10000, include_print=True):
    participantsOrder = [[0,1,2], [0,1,2,3,3,3,4,2,2,2]]
    sum = 0
    numTxn = 0
    for i, participantIndex in enumerate(participantsOrder[cond - 1]):
    # for i, participantIndex in enumerate(tmp_order):
        if i >= starting_step and i <= limit:
            args = [i]
            if i == 1:
                args.append(cond)
            elif cond == 2 and i == 2:
                args.append(to_distributor_amount)
                args.append(to_manufacturer_amount)
            elif cond == 2 and (i == 7 or i == 8):
                # confirmation
                args.append(1)
            elapsed_time = execute_transaction(app_id, accounts[participantIndex], args=args, accounts=extract_addresses(accounts, [2,3,4]), include_print=include_print)
            if i == 1:
                payment_transaction(accounts[2], app_address, to_distributor_amount + to_manufacturer_amount)
                payment_transaction(accounts[3], app_address, to_distributor_amount)
            if i == 2:
                execute_transaction(app_id, accounts[2], args=[100], accounts=extract_addresses(accounts, [2,3,4]), include_print=include_print)
                execute_transaction(app_id, accounts[4], args=[200], accounts=extract_addresses(accounts, [2,3,4]), include_print=include_print)
            sum += elapsed_time
            numTxn += 1
    return sum / numTxn

def get_application_balance(app_id):
    contract_escrow_address = logic.get_application_address(app_id)
    account_info = client.account_info(contract_escrow_address)
    balance = account_info['amount']
    print("Balance:", balance, "microAlgos")
    return balance
    
def get_application_address(app_id):
    contract_escrow_address = logic.get_application_address(app_id)
    print("Contract Escrow Address:", contract_escrow_address)
    return contract_escrow_address

def print_234_balance():
    print("Account 3: " + str(client.account_info(testnet_accounts[3]["address"])["amount"]))
    print("Account 2: " + str(client.account_info(testnet_accounts[2]["address"])["amount"]))
    print("Account 4: " + str(client.account_info(testnet_accounts[4]["address"])["amount"]))

def opt_int(app_id, sender):
    params = client.suggested_params()

    txn = transaction.ApplicationOptInTxn(
        sender=sender["address"],
        sp=params,
        index=app_id,  # Application ID
    )

    # Sign and send the transaction
    signed_txn = txn.sign(sender["private_key"])
    tx_id = client.send_transaction(signed_txn)
    transaction.wait_for_confirmation(client, tx_id, 2)
    print(f"Opt-in transaction sent with txid: {tx_id}")

def testing_timestamp(app_id, accounts, account_index, args, include_print=True):
    execute_transaction(app_id, accounts[account_index], args=args, accounts=extract_addresses(accounts, [2,3,4]), include_print=include_print)

def test_payment_transaction():
    total = 0
    for i in range(5):
        elapsed_time = payment_transaction(testnet_accounts[5], testnet_accounts[6]["address"], 2000)
        print(elapsed_time)
        total += elapsed_time
    print("Avg time: ", total/5)

def run():
    # print(get_wallet_accounts())
    acc = create_account()
    # print(create_account())
    fund_accounts([acc])
    print(get_balance(acc))
    app_id = initialize_tmp_contract([acc], 0, True)
    print(app_id)
    
    # app_id = 731748739 # ProcessExecutionSimpleContract
    # app_id = 731992167 # ProcessExecutionOrderMedication
    
    # app_id = 731992965 # sa upotrebom Txn.application_args.length() 
    # app_id = 732006016 # bez Txn.application_args.length()
    # app_id = 732006111 # bez get_cond() i Txn.application_args.length()
    # app_id = 732134711
    
    
    
    # print(run_correct_test_simple_contract(testnet_accounts, app_id))
    
    # print("Average txn time: ", run_correct_test_simple_contract(testnet_accounts, app_id))
    
    
    # print(client.account_info(testnet_accounts[3]["address"])["amount"]) 
    # print(client.account_info("EPZDB4LQQZD367RSPNLGKYIVKCQGGDRZQSNONZGTXLHDPIPAEHMV3ES4JQ")["amount"])
    
    # print(testnet_accounts[2]["address"])
    # app_id = initialize_contract(testnet_accounts, 5, False)
    # print(app_id)
    # get_application_address(app_id)
    # app_id = 732141586
    # testing_timestamp(app_id, testnet_accounts, 2, [101])
    # testing_timestamp(app_id, testnet_accounts, 2, [100, 2])
    # testing_timestamp(app_id, testnet_accounts, 2, [200])
    # print_234_balance()
    
    # payment_transaction(testnet_accounts[2], app_address, to_distributor_amount + to_manufacturer_amount)
    # payment_transaction(testnet_accounts[3], app_address, to_distributor_amount)
    
    
    # print_234_balance()
    # to_distributor_amount=1000
    # to_manufacturer_amount=to_distributor_amount+4000+1000
    # run_correct_test_order_medication_contract(testnet_accounts[:5], app_id, 2, app_address=get_application_address(app_id),  to_distributor_amount=to_distributor_amount, to_manufacturer_amount=to_manufacturer_amount, starting_step=0, limit=2)
    # reset_state(app_id, testnet_accounts[0])
    
    # print_234_balance()
    
    # print(get_balance(testnet_accounts[0]))
    # app_ids = []
    # for i in range(473):
    #     app_id = initialize_contract(testnet_accounts, 0, False)
    #     print(app_id)
    #     app_ids.append(app_id)
    
    # print(app_ids)
    # print(calculate_total_balance(testnet_accounts))
    # key, addr = accounts[0]
    
    # app_id = 731748739
    # reset_state(app_id, testnet_accounts[0])
    # run_correct_test_simple_contract(testnet_accounts, 731748739)
    
    # participantsOrder = [0, 1, 2, 3, 4, 2, 2]
    # startSum = calculate_total_balance(accounts)
    # print(calculate_total_balance(accounts))
    
    # for (let i = 0; i < 7; i++) {
    #     const enactTx = await contract.connect(signers[participantsOrder[i]]).enact(i)
    #     const txData = await enactTx.wait()
    # }
    # const endSum = await calculateTotalBalance(signers)
    # console.log("Total gas spent: ", startSum - endSum);
    
    # make_transaction(testnet_app_id, testnet_accounts[0], id=0, include_print=True)
    # make_transaction(app_id, accounts[1], id=1)
    # make_transaction(app_id, accounts[2], id=2)
    # make_transaction(app_id, accounts[1], id=2)
    # print(calculate_total_balance(accounts))
    
    # network_status = client.status()
    # print("Genesis ID:", network_status)
    
        # for acc in testnet_accounts:
    #     print(client.account_info(acc["address"])["amount"])
    # print(address)
    # algosdk.generate_acccount()
    # print(create_account())
    
    # addresses = {}
    # for i, a in enumerate(extract_addresses(testnet_accounts)):
    #     addresses["address" + str(i)] = a
    # print(addresses)
    # modify_template_file("/home/lazar/Documents/Seminar blockchain/contracts/algorand/pyteal/ProcessExecution.py", data=addresses)
    pass
    
run()
