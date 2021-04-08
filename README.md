# Akropolis+Yearn 

Solidity contracts used in [Akropolis Delphi](https://delphi.akropolis.io/) yearn pools.


## Testing and Development

### Dependencies

* [python3](https://www.python.org/downloads/release/python-368/) version 3.6 or greater, python3-dev
* [brownie](https://github.com/iamdefinitelyahuman/brownie) - tested with version [1.12.0](https://github.com/eth-brownie/brownie/releases/tag/v1.12.0)
* [ganache-cli](https://github.com/trufflesuite/ganache-cli) - tested with version [6.11.0](https://github.com/trufflesuite/ganache-cli/releases/tag/v6.11.0)

Delphi contracts are compiled using [Solidity], however installation of the required Solidity versions is handled by Brownie.

### Setup

To get started, first create and initialize a Python [virtual environment](https://docs.python.org/3/library/venv.html). Next, clone the repo and install the developer dependencies:

```bash
git clone https://github.com/akropolisio/delphi-yearn.git
cd contracts
pip install -r requirements.txt
```

Run the command:
```bash
npm install
```
It executes several intallation steps:
* install all npm dependencies
* install all python dependencies (if not installed yet) including Brownie framework
* install Brownie dependency packages (openzeppelin and yearn)
* copy these packages to the working directory (see explanation below)
* compile contracts
* generate abi artifaacts (if needed)


Due to the existing [bug in Brownie framework](https://github.com/eth-brownie/brownie/issues/893) you may need to install the packages manually:
```
npm run clone-packages
```

### Running the Tests

To run the entire suite:

```bash
brownie test
```

### Security tools

See [the instruction for running security tools](security/readme.md) upon Akropolis Delphi protocol.
Slither, Echidna and Manticore are integrated.


### Deployment
Create *.env* file with *DEPLOYER_PRIVATE_KEY* filled up.
*.env* file also should contain *ADMIN_PRIVATE_KEY* in case of human-admin or *PROXY_ADMIN_ADDRESS* in case of AdminProxy contract already deployed. Leave both variables empty if new AdminProxy contract should be deployed.

For the local deployment run the command:

```bash
npm run deploy:devV1
```
or 
```bash
brownie run deploy_vault_savingsV1.py
```

For the *Rinkeby* deployment firstly export Infura id:

```bash
export WEB3_INFURA_PROJECT_ID=b20c30c9e04c4a6bb1cd728ff589a15e
```

and run:

```bash
npm run deploy:rinkebyV1
```
or 
```bash
brownie run deploy_vault_savingsV1.py --network rinkeby
```

### Fork Mainnet
In order to perform mainnet-fork testing in automatic way you should perform next actions:

1) If you want to work with Alchemy node (instead of slow Infurra node), first of all export host address (for example):
```bash
export ALCHEMY_ARCHIVE_NODE=https://eth-mainnet.alchemyapi.io/v2/3MsO_qdMuAz1ILi6KhiNZ-UO6lqq5mtA
```
2) Infura project ID
```bash
export WEB3_INFURA_PROJECT_ID=<YOUR_PROJECT_ID>
```
3) Also you need to export Etherscan token in order to be able to fetch the data (to get enough requests attempts):
```bash
export ETHERSCAN_TOKEN=<YOUR_ETHER_SCAN_TOKEN>
```
4) After that add it to the mainnet-fork configuration:
```bash
npm run test:add-fork
```

Now you can run the test:
```bash
npm run test:swap-mainnet

npm run test:indices-mainnet
```

Or you can run the console with the free emulation:
```bash
brownie console --network mainnet-fork
```

## License

Copyright (c) 2020 A Labs Ltd., AGPL V3.0
