// SPDX-License-Identifier: AGPL V3.0

pragma solidity >=0.6.0 <0.8.0;

pragma experimental ABIEncoderV2;

import "@openzeppelinV3/contracts/token/ERC20/IERC20.sol";
import "@openzeppelinV3/contracts/token/ERC20/SafeERC20.sol";
import "@openzeppelinV3/contracts/utils/Address.sol";
import "@openzeppelinV3/contracts/math/SafeMath.sol";
import "@openzeppelinV3/contracts/Access/Ownable.sol";
import "@openzeppelinV3/contracts/utils/ReentrancyGuard.sol";

import "../../../interfaces/yearnV1/IVault.sol";
import "../../../interfaces/yearnV1/IVaultSavings.sol";


contract VaultSavings is IVaultSavings, Ownable, ReentrancyGuard {

    uint256 constant MAX_UINT256 = uint256(-1);

    using SafeERC20 for IERC20;
    using Address for address;
    using SafeMath for uint256;

    struct VaultInfo {
        bool isActive;
        uint256 blockNumber;
    }

    address[] internal registeredVaults;
    mapping(address => VaultInfo) vaults;

    
    // deposit, withdraw

    function deposit(address[] calldata _vaults, uint256[] calldata _amounts) external override nonReentrant  {
        require(_vaults.length == _amounts.length, "Size of arrays does not match");

        for (uint256 i=0; i < _vaults.length; i++) {
            _deposit(_vaults[i], _amounts[i]);
        }
    }

    function deposit(address _vault, uint256 _amount) external override nonReentrant returns(uint256 lpAmount) {
        lpAmount = _deposit(_vault, _amount);
    }
   

    function _deposit(address _vault, uint256 _amount) internal returns(uint256 lpAmount) {
        //check vault
        require(isVaultRegistered(_vault), "Vault is not Registered");

        address baseToken = IVault(_vault).token();
     
        //transfer token if it is allowed to contract
        IERC20(baseToken).safeTransferFrom(msg.sender, address(this), _amount);

        //set allowence to vault
        IERC20(baseToken).safeIncreaseAllowance(_vault, _amount);

        //deposit token to vault
        IVault(_vault).deposit(_amount);

        lpAmount = IERC20(_vault).balanceOf(address(this));
        //send new tokens to user
        IERC20(_vault).safeTransfer(msg.sender, lpAmount);

        emit  Deposit(_vault, msg.sender, _amount, lpAmount);
    }


    function withdraw(address[] calldata _vaults, uint256[] calldata _amounts) external override nonReentrant {
        require(_vaults.length == _amounts.length, "Size of arrays does not match");

        for (uint256 i=0; i < _vaults.length; i++) {
            _withdraw(_vaults[i], _amounts[i]);
        }

    }

    function withdraw(address _vault, uint256 _amount) external override nonReentrant returns(uint256 baseAmount) {
        baseAmount = _withdraw(_vault, _amount);
    }

    function _withdraw(address _vault, uint256 _amount) internal returns(uint256 baseAmount) {
        require(isVaultRegistered(_vault), "Vault is not Registered");
        //transfer LP Token if it is allowed to contract
        IERC20(_vault).safeTransferFrom(msg.sender, address(this), _amount);

        //burn tokens from vault
        IVault(_vault).withdraw(_amount);

        address baseToken = IVault(_vault).token();

        baseAmount = IERC20(baseToken).balanceOf(address(this));

        //Transfer token to user
        IERC20(baseToken).safeTransfer(msg.sender, baseAmount);

        emit Withdraw(_vault, msg.sender, baseAmount, _amount);
    }

    function registerVault(address _vault) external override onlyOwner {
        require(!isVaultRegistered(_vault), "Vault is already registered");

        registeredVaults.push(_vault);

        vaults[_vault] = VaultInfo({
            isActive: true,
            blockNumber: block.number
        });

        address baseToken = IVault(_vault).token();

        emit VaultRegistered(_vault, baseToken);
    }

    function activateVault(address _vault) external override onlyOwner {
        require(isVaultRegistered(_vault), "Vault is not registered");
    
        vaults[_vault] = VaultInfo({
            isActive: true,
            blockNumber: block.number
        });

       emit VaultActivated(_vault);

    }

    function deactivateVault(address _vault) external override onlyOwner {
        require(isVaultRegistered(_vault), "Vault is not registered");
    
        vaults[_vault] = VaultInfo({
            isActive: false,
            blockNumber: block.number
        });

       emit VaultDisabled(_vault);
    }
    

    //view functions
    function isVaultRegistered(address _vault) public override view returns(bool) {
        for (uint256 i = 0; i < registeredVaults.length; i++){
            if (registeredVaults[i] == _vault) return true;
        }
        return false;
    }

    function isVaultActive(address _vault) public override view returns(bool) {

        return vaults[_vault].isActive;
    }

    function isBaseTokenForVault(address _vault, address _token) public override view returns(bool) {
        address baseToken = IVault(_vault).token();
        if (baseToken == _token) return true;
        return false;
    }

    function supportedVaults() external override view returns(address[] memory) {
        return registeredVaults;
    }

    function activeVaults()  external override view returns(address[] memory _vaults) {  
        uint256 j = 0;
        for (uint256 i = 0; i < registeredVaults.length; i++) {
            if (vaults[registeredVaults[i]].isActive) {
                j = j.add(1);
            }
        }
        if (j > 0) {
            _vaults = new address[](j);
            j = 0;
            for (uint256 i = 0; i < registeredVaults.length; i++) {
                if (vaults[registeredVaults[i]].isActive) {
                    _vaults[j] = registeredVaults[i]; 
                    j = j.add(1);
                }
            }
        }
    }   
}