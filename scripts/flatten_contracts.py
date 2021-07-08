import sys
from os import path
from brownie import *


def _flattener(contracts_to_flatten):
    for contract_obj in contracts_to_flatten:
        contract_info = contract_obj.get_verification_info()
        flatten_file_name = path.join(
            "flattened", ".".join([contract_obj._name, "sol"])
        )
        with open(flatten_file_name, "w") as fl_file:
            fl_file.write(contract_info["flattened_source"])


def main():
<<<<<<< HEAD
    contracts_to_flatten = [
        VaultSavings,
        VestedAkro,
        AdelVAkroSwap,
        AdelVAkroVestingSwap,
        UtilProxy,
        UtilProxyAdmin,
        ExploitCompVAkroSwap,
        Rewards

    ]
=======
    contracts_to_flatten = [ExploitCompVAkroSwap, VestedAkro, VaultSavings, VestedAkro, AdelVAkroSwap, AdelVAkroVestingSwap, UtilProxy, UtilProxyAdmin]
>>>>>>> 740936facf19f5b26c277c6c246d3d6e3ebfa072
    _flattener(contracts_to_flatten)


def echidna():
    contracts_to_flatten = [TestVaultSavings]
    _flattener(contracts_to_flatten)
