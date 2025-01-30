import json
from concurrent.futures import ThreadPoolExecutor
import time

import Client as client

def my_function(instance_id, app_id, accounts):
    print(instance_id)
    avg_transaction_time = client.run_correct_test_simple_contract(accounts, app_id, include_print=False)
    return {
        "instance_id": instance_id,
        "avg_transaction_time": avg_transaction_time
    }

def reset_state(instance_id, app_id, sender):
    print(instance_id)
    client.reset_state(app_id, sender)

num_instances = 50

with ThreadPoolExecutor(max_workers=num_instances) as executor:
    futures = []
    for i in range(num_instances):
        app_id = client.testnet_app_ids[i]
        time.sleep(1)
        futures.append(executor.submit(my_function, i, app_id, client.testnet_accounts))
    
    # for i in range(num_instances):
    #     app_id = client.testnet_app_ids[i]
    #     time.sleep(1)
    #     futures.append(executor.submit(reset_state, i, app_id, client.testnet_accounts[0]))

results = [future.result() for future in futures]

total = 0
for r in results:
    total += r["avg_transaction_time"]
print("Average transaction time: ", str(total/len(results)))
with open("scalability_final_test_results/scalability_test_results_" + str(num_instances) + "_no_print.json", "w") as file:
    json.dump(results, file, indent=4)

print("All instances completed!")
