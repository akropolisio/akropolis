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
npm run deploy:dev
```
or 
```bash
brownie run deploy_vault_savings.py
```

For the *Rinkeby* deployment firstly export Infura id:

```bash
export WEB3_INFURA_PROJECT_ID=b20c30c9e04c4a6bb1cd728ff589a15e
```

and run:

```bash
npm run deploy:rinkeby
```
or 
```bash
brownie run deploy_vault_savings.py --network rinkeby
```




## License

Copyright (c) 2020 Akropolis, AGPL V3.0
