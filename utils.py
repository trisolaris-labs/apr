import json

FACTORY_ADDRESS = "0xc66F594268041dB60507F00703b152492fb176E7"
CHEF_ADDRESS = "0x474b825a605c45836Ac50398473059D4c4c6d3Db"
WETH_ADDRESS = "0xC9BdeEd33CD01541e1eeD10f90519d2C06Fe3feB"
WNEAR_ADDRESS = "0xc42c30ac6cc15fac9bd938618bcaa1a1fae8501d"
USDC_ADDRESS = "0xB12BFcA5A55806AaF64E99521918A4bf0fC40802"
TRI_ADDRESS = "0x0029050f71704940D77Cfe71D0F1FB868DeeFa03"
DAI_ADDRESS = "0xe3520349f477a5f6eb06107066048508498a291b"

DAI_USDC = "0xbb310Ef4Fac855f2F49D8Fb35A2DA8f639B3464E"
WNEAR_USDC = "0x20F8AeFB5697B77E0BB835A8518BE70775cdA1b0"
TRI_USDC = "0x56ff686187cffbB09E545655F88CCaB690D77cE2"

def init_chef(w3):
    with open(f'chef.json') as json_file:
        return w3.eth.contract(
            address=CHEF_ADDRESS,
            abi=json.load(json_file)
        )

def init_tlp(w3, lpAddress):
    with open(f'tlp.json') as json_file:
        return w3.eth.contract(
            address=lpAddress,
            abi=json.load(json_file)
        )

def reserveInUsdc(tlp):
    t0 = tlp.functions.token0().call()
    t1 = tlp.functions.token1().call()
    reserves = tlp.functions.getReserves().call()
    if (t0 == USDC_ADDRESS | t1 == USDC_ADDRESS):
        