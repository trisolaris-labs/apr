def get_abi(contract):
    abi_file_path = f"contract.json"
    with open(f'{abi_file_path}/{contract}.json') as json_file:
        return json.load(json_file)


def initialize_contract(w3, contract_address, contract_name):
    return w3.eth.contract(
        address=contract_address,
        abi=get_abi(contract_name)
    )