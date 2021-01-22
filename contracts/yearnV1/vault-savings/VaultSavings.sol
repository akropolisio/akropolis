// SPDX-License-Identifier: AGPL V3.0

pragma solidity >=0.6.0 <0.8.0;

pragma experimental ABIEncoderV2;

import "@ozUpgradesV3/contracts/token/ERC20/IERC20Upgradeable.sol";
import "@ozUpgradesV3/contracts/token/ERC20/SafeERC20Upgradeable.sol";
import "@ozUpgradesV3/contracts/utils/AddressUpgradeable.sol";
import "@ozUpgradesV3/contracts/math/SafeMathUpgradeable.sol";
import "@ozUpgradesV3/contracts/access/OwnableUpgradeable.sol";
import "@ozUpgradesV3/contracts/utils/ReentrancyGuardUpgradeable.sol";

import "../../../interfaces/yearnV1/IVault.sol";
import "../../../interfaces/yearnV1/IVaultSavings.sol";
import "../../../interfaces/curvefi/ICurveFiDeposit.sol";
import "../../../interfaces/curvefi/ICurveFiDeposit3.sol";
import "../../../interfaces/curvefi/ICurveFiDeposit4.sol";
import "../../utils/ArrayConversions.sol";


import "@ozUpgradesV3/contracts/utils/PausableUpgradeable.sol";

contract VaultSavings is IVaultSavings, OwnableUpgradeable, ReentrancyGuardUpgradeable, PausableUpgradeable {

    uint256 constant MAX_UINT256 = uint256(-1);

    using SafeERC20Upgradeable  for IERC20Upgradeable;
    using AddressUpgradeable for address;
    using SafeMathUpgradeable for uint256;

    struct CurveFiInfo {
        address deposit;
        address[] tokens;
    }

    struct VaultInfo {
        bool isActive;
        uint256 blockNumber;
        CurveFiInfo curveFi;
    }

    address[] internal registeredVaults;
    mapping(address => VaultInfo) vaults;

    function initialize() public initializer {
        __Ownable_init();
        __ReentrancyGuard_init();
        __Pausable_init();
    }

    
    // deposit, withdraw

    function deposit(address[] calldata _vaults, address[][] calldata _tokens, uint256[][] calldata _amounts, uint256[] calldata minConvertAmounts) external override nonReentrant whenNotPaused 
    returns(uint256[] memory amounts) {
        require(_vaults.length > 0, "Nothing to deposit");
        require(_vaults.length == _tokens.length, "Size of tokens array does not match vaults");
        require(_vaults.length == _amounts.length, "Size of amounts array does not match vaults");

        amounts = new uint256[](_vaults.length);
        for(uint256 i=0; i<_vaults.length; i++){
            require(_tokens[i].length == _amounts[i].length, "Size of tokens array does not match amounts");
            (amounts[i],) = _deposit_one_vault(_vaults[i], _tokens[i], _amounts[i], minConvertAmounts[i]);
        }
    }

    function _deposit_one_vault(address _vault, address[] memory _tokens, uint256[] memory _amounts, uint256 minConvertAmount) internal 
    returns(uint256 baseAmount, uint256 lpAmount) {
        require(isVaultRegistered(_vault), "Vault is not Registered");
        
        CurveFiInfo storage cf = vaults[_vault].curveFi;

        address baseToken = IVault(_vault).token();

        uint256[] memory amnts = new uint256[](cf.tokens.length);
        bool cfDepositRequired;
        for(uint256 t=0; t<_tokens.length; t++){
            if(_tokens[t] == baseToken){
                baseAmount = _amounts[t];
            }else{
                uint256 pos = _getCurveFiTokenPosition(cf, _tokens[t]);
                amnts[pos] = _amounts[t];
                if(amnts[pos] > 0) cfDepositRequired = true;
            }
        }

        if(baseAmount > 0){
            IERC20Upgradeable(baseToken).safeTransferFrom(msg.sender, address(this), baseAmount);
        }

        if(cfDepositRequired){
            uint256 convertedAmount = _curveFiDeposit(cf, baseToken, amnts, minConvertAmount);
            baseAmount = baseAmount.add(convertedAmount);
        }


        IERC20Upgradeable(baseToken).safeIncreaseAllowance(_vault, baseAmount);
        IVault(_vault).deposit(baseAmount);

        lpAmount = IERC20Upgradeable(_vault).balanceOf(address(this));
        IERC20Upgradeable(_vault).safeTransfer(msg.sender, lpAmount);

        emit  Deposit(_vault, msg.sender, baseAmount, lpAmount);

    }

    function _curveFiDeposit(CurveFiInfo storage cf, address cfLPToken, uint256[] memory _amounts, uint256 _minCurveLPAmount) internal 
    returns(uint256 curveLPAmount){
        // Transfer underlying tokens
        for(uint256 i=0; i<cf.tokens.length; i++){
            if(_amounts[i] > 0){
                IERC20Upgradeable(cf.tokens[i]).safeTransferFrom(msg.sender, address(this), _amounts[i]);
            }
        }

        //NOTE: cf.deposit is trusted contract and we have nonReentrant modifier on top level
        uint256 balanceBefore = IERC20Upgradeable(cfLPToken).balanceOf(address(this));
        if(_amounts.length == 4){
            ICurveFiDeposit4(cf.deposit).add_liquidity(ArrayConversions.convertUint256Array4(_amounts), _minCurveLPAmount);
        }else if(_amounts.length == 3) {
            ICurveFiDeposit3(cf.deposit).add_liquidity(ArrayConversions.convertUint256Array3(_amounts), _minCurveLPAmount);
        }
        uint256 balanceAfter = IERC20Upgradeable(cfLPToken).balanceOf(address(this));
        curveLPAmount = balanceAfter.sub(balanceBefore);
        emit CurveDeposit(cf.deposit, msg.sender, _amounts, curveLPAmount);
    }

    function deposit(address[] calldata _vaults, uint256[] calldata _amounts) external override nonReentrant whenNotPaused {
        require(_vaults.length == _amounts.length, "Size of arrays does not match");

        for (uint256 i=0; i < _vaults.length; i++) {
            _deposit(_vaults[i], _amounts[i]);
        }
    }

    function deposit(address _vault, uint256 _amount) external override nonReentrant whenNotPaused returns(uint256 lpAmount)  {
        lpAmount = _deposit(_vault, _amount);
    }
   

    function _deposit(address _vault, uint256 _amount) internal returns(uint256 lpAmount) {
        //check vault
        require(isVaultRegistered(_vault), "Vault is not Registered");

        address baseToken = IVault(_vault).token();
     
        //transfer token if it is allowed to contract
        IERC20Upgradeable(baseToken).safeTransferFrom(msg.sender, address(this), _amount);

        //set allowence to vault
        IERC20Upgradeable(baseToken).safeIncreaseAllowance(_vault, _amount);

        //deposit token to vault
        IVault(_vault).deposit(_amount);

        lpAmount = IERC20Upgradeable(_vault).balanceOf(address(this));
        //send new tokens to user
        IERC20Upgradeable(_vault).safeTransfer(msg.sender, lpAmount);

        emit  Deposit(_vault, msg.sender, _amount, lpAmount);
    }

    function withdraw(address[] calldata _vaults, address[][] calldata _tokens, uint256[][] calldata _amounts, uint256[] calldata maxConvertAmounts) external nonReentrant whenNotPaused {
        require(_vaults.length > 0, "Nothing to withdraw");
        require(_vaults.length == _tokens.length, "Size of tokens array does not match vaults");
        require(_vaults.length == _amounts.length, "Size of amounts array does not match vaults");

        for(uint256 i=0; i<_vaults.length; i++){
            require(_tokens[i].length == _amounts[i].length, "Size of tokens array does not match amounts");
            //_withdraw_one_vault(_vaults[i], _tokens[i], _amounts[i], minConvertAmounts[i]);
        }
    
    }

    function _withdraw_one_vault(address _vault, address[] memory _tokens, uint256[] memory _amounts, uint256 maxConvertAmount) internal 
    returns(uint256){
        CurveFiInfo storage cf = vaults[_vault].curveFi;

        address baseToken = IVault(_vault).token();
        uint256 baseAmount;

        uint256[] memory amnts = new uint256[](cf.tokens.length);
        bool cfWithdrawRequired;
        for(uint256 t=0; t<_tokens.length; t++){
            if(_tokens[t] == baseToken){
                baseAmount = _amounts[t];
            }else{
                uint256 pos = _getCurveFiTokenPosition(cf, _tokens[t]);
                amnts[pos] = _amounts[t];
                if(amnts[pos] > 0) cfWithdrawRequired = true;
            }
        }
        
        uint256 fullWithdrawAmount = baseAmount;
        uint256 cfWithdrawAmount;
        if(cfWithdrawRequired) {
            cfWithdrawAmount = (maxConvertAmount != 0)? maxConvertAmount : _curveFiCalculateWithdrawAmount(cf, amnts);
            fullWithdrawAmount = fullWithdrawAmount.add(cfWithdrawAmount);
        }
        

        uint256 withdrawShares = IVault(_vault).getPricePerFullShare().mul(fullWithdrawAmount);
        IERC20Upgradeable(_vault).safeTransferFrom(msg.sender, address(this), withdrawShares);
        IVault(_vault).withdraw(withdrawShares);
        emit Withdraw(_vault, msg.sender, fullWithdrawAmount, withdrawShares);

        if(baseAmount > 0) {
            IERC20Upgradeable(baseToken).safeTransfer(msg.sender, baseAmount);
        }
        if(cfWithdrawRequired){
            uint256 curveLPAmount = _curveFiWithdraw(cf, baseToken, amnts, cfWithdrawAmount);
        }

        // uint256 curveLPLeft = IERC20Upgradeable(baseToken).balanceOf(address(this));
        // TODO: somehow handle this tokens

    }

    function _curveFiCalculateWithdrawAmount(CurveFiInfo storage cf, uint256[] memory amounts) internal returns(uint256 withdrawAmount) {
        ICurveFiDeposit cfd = ICurveFiDeposit(cf.deposit);
        for(uint256 i=0; i<amounts.length; i++){
            withdrawAmount = withdrawAmount.add(cfd.calc_withdraw_one_coin(amounts[i], int128(i)));
        }
    }


    function _curveFiWithdraw(CurveFiInfo storage cf, address cfLPToken, uint256[] memory _amounts, uint256 _maxCurveLPAmount) internal 
    returns(uint256 curveLPAmount){

        //NOTE: cf.deposit is trusted contract and we have nonReentrant modifier on top level
        uint256 balanceBefore = IERC20Upgradeable(cfLPToken).balanceOf(address(this));
        if(_amounts.length == 4){
            ICurveFiDeposit4(cf.deposit).remove_liquidity_imbalance(ArrayConversions.convertUint256Array4(_amounts), _maxCurveLPAmount);
        }else if(_amounts.length == 3) {
            ICurveFiDeposit3(cf.deposit).remove_liquidity_imbalance(ArrayConversions.convertUint256Array3(_amounts), _maxCurveLPAmount);
        }
        uint256 balanceAfter = IERC20Upgradeable(cfLPToken).balanceOf(address(this));
        curveLPAmount = balanceAfter.sub(balanceBefore);


        // Transfer underlying tokens
        for(uint256 i=0; i<cf.tokens.length; i++){
            if(_amounts[i] > 0){
                IERC20Upgradeable(cf.tokens[i]).safeTransfer(msg.sender, _amounts[i]);
            }
        }
        emit CurveWithdraw(cf.deposit, msg.sender, _amounts, curveLPAmount);
    }


    function withdraw(address[] calldata _vaults, uint256[] calldata _amounts) external override nonReentrant whenNotPaused {
        require(_vaults.length == _amounts.length, "Size of arrays does not match");

        for (uint256 i=0; i < _vaults.length; i++) {
            _withdraw(_vaults[i], _amounts[i]);
        }

    }

    function withdraw(address _vault, uint256 _amount) external override nonReentrant whenNotPaused returns(uint256 baseAmount) {
        baseAmount = _withdraw(_vault, _amount);
    }

    function _withdraw(address _vault, uint256 _amount) internal returns(uint256 baseAmount) {
        require(isVaultRegistered(_vault), "Vault is not Registered");
        //transfer LP Token if it is allowed to contract
        IERC20Upgradeable(_vault).safeTransferFrom(msg.sender, address(this), _amount);

        //burn tokens from vault
        IVault(_vault).withdraw(_amount);

        address baseToken = IVault(_vault).token();

        baseAmount = IERC20Upgradeable(baseToken).balanceOf(address(this));

        //Transfer token to user
        IERC20Upgradeable(baseToken).safeTransfer(msg.sender, baseAmount);

        emit Withdraw(_vault, msg.sender, baseAmount, _amount);
    }

    function registerVault(address _vault, address _cfDeposit, uint256 tokensCount) external override onlyOwner {
        require(!isVaultRegistered(_vault), "Vault is already registered");

        registeredVaults.push(_vault);

        address[] memory tkns = new address[](tokensCount);
        for(uint256 i=0; i<tokensCount; i++){
            tkns[i] = ICurveFiDeposit(_cfDeposit).underlying_coins(int128(i));
        }

        vaults[_vault] = VaultInfo({
            isActive: true,
            blockNumber: block.number,
            curveFi: CurveFiInfo({
                deposit: _cfDeposit,
                tokens: tkns
            })
        });

        address baseToken = IVault(_vault).token();

        emit VaultRegistered(_vault, baseToken);
    }

    function activateVault(address _vault) external override onlyOwner {
        require(isVaultRegistered(_vault), "Vault is not registered");
    
        vaults[_vault].isActive = true;
        vaults[_vault].blockNumber = block.number;

       emit VaultActivated(_vault);

    }

    function deactivateVault(address _vault) external override onlyOwner {
        require(isVaultRegistered(_vault), "Vault is not registered");
    
        vaults[_vault].isActive = false;
        vaults[_vault].blockNumber = block.number;

       emit VaultDisabled(_vault);
    }

    function pause() external onlyOwner {
        _pause();
    }

    function unpause() external onlyOwner {
        _unpause();
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

    function _getCurveFiTokenPosition(CurveFiInfo storage cf, address token) internal returns(uint256) {
        for(uint256 i=0; i<cf.tokens.length; i++){
            if(cf.tokens[i] == token) return i;
        }
        revert("Token not found in CurveFi");
    }

}