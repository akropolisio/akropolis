// SPDX-License-Identifier: AGPL V3.0
pragma solidity ^0.6.12;

import "@ozUpgradesV3/contracts/access/OwnableUpgradeable.sol";
import "@ozUpgradesV3/contracts/token/ERC20/IERC20Upgradeable.sol";
import "@ozUpgradesV3/contracts/math/SafeMathUpgradeable.sol";
import "@ozUpgradesV3/contracts/token/ERC20/SafeERC20Upgradeable.sol";
import "./MinterRole.sol";
import "./VestedAkroSenderRole.sol";

/**
 * @notice VestedAkro token represents AKRO token vested for a vestingPeriod set by owner of this VestedAkro token.
 * Generic holders of this token CAN NOT transfer it. They only can redeem AKRO from unlocked vAKRO.
 * Minters can mint unlocked vAKRO from AKRO to special VestedAkroSenders.
 * VestedAkroSender can send his unlocked vAKRO to generic holders, and this vAKRO will be vested. He can not redeem AKRO himself.
 */
contract VestedAkro is OwnableUpgradeable, IERC20Upgradeable, MinterRole, VestedAkroSenderRole {
    using SafeMathUpgradeable for uint256;
    using SafeERC20Upgradeable for IERC20Upgradeable;

    event Locked(address indexed holder, uint256 amount);
    event Unlocked(address indexed holder, uint256 amount);
    event AkroAdded(uint256 amount);

    struct VestedBatch {
        uint256 amount;     // Full amount of vAKRO vested in this batch
        uint256 start;      // Vesting start time;
        uint256 end;        // Vesting end time
        uint256 claimed;    // vAKRO already claimed from this batch to unlocked balance of holder
    }

    struct Balance {
        VestedBatch[] batches;  // Array of vesting batches
        uint256 locked;         // Amount locked in batches
        uint256 unlocked;       // Amount of unlocked vAKRO (which either was previously claimed, or received from Minter)
        uint256 firstUnclaimedBatch; // First batch which is not fully claimed
    }

    string private _name;
    string private _symbol;
    uint8 private _decimals;

    uint256 public override totalSupply;
    IERC20Upgradeable public akro;
    uint256 public vestingPeriod; //set by owner of this VestedAkro token
    uint256 public vestingStart; //set by owner, default value 01 May 2021, 00:00:00 GMT+0
    uint256 public vestingCliff; //set by owner, cliff for akro unlock, 1 month by default
    mapping (address => mapping (address => uint256)) private allowances;
    mapping (address => Balance) private holders;


    function initialize(address _akro, uint256 _vestingPeriod) public initializer {
        __Ownable_init();
        MinterRole.initialize(_msgSender());
        VestedAkroSenderRole.initialize(_msgSender());

        _name = "Vested AKRO";
        _symbol = "vAKRO";
        _decimals = 18;
        
        akro = IERC20Upgradeable(_akro);
        require(_vestingPeriod > 0, "VestedAkro: vestingPeriod should be > 0");
        vestingPeriod = _vestingPeriod;
        vestingStart = 1619827200; //01 May 2021, 00:00:00 GMT+0
        vestingCliff = 31 * 24 * 60 * 60; //1 month - 31 day in May
    }

    // Stub for compiler purposes only
    function initialize(address sender) public override(MinterRole, VestedAkroSenderRole) {
    }

    function name() public view returns (string memory) {
        return _name;
    }

    function symbol() public view returns (string memory) {
        return _symbol;
    }

    function decimals() public view returns (uint8) {
        return _decimals;
    }

    function allowance(address owner, address spender) public override view returns (uint256) {
        return allowances[owner][spender];
    }

    /// if_succeeds {:msg "wrong spender"} spender != address(0);
    function approve(address spender, uint256 amount) public override returns (bool) {
        _approve(_msgSender(), spender, amount);
        return true;
    }

    /// if_succeeds {:msg "only sender"} isSender(msg.sender);
    function transferFrom(address sender, address recipient, uint256 amount) public override onlySender returns (bool) {
        // We require both sender and _msgSender() to have VestedAkroSender role
        // to prevent sender from redeem and prevent unauthorized transfers via transferFrom.
        require(isSender(sender), "VestedAkro: sender should have VestedAkroSender role");

        _transfer(sender, recipient, amount);
        _approve(sender, _msgSender(), allowances[sender][_msgSender()].sub(amount, "VestedAkro: transfer amount exceeds allowance"));
        return true;
    }

    /// if_succeeds {:msg "only sender"} isSender(msg.sender);
    function transfer(address recipient, uint256 amount) public override onlySender returns (bool) {
        _transfer(_msgSender(), recipient, amount);
        return true;
    }

    /// if_succeeds {:msg "VestedAkro: vestingPeriod should be > 0"} _vestingPeriod > 0;
    /// if_succeeds {:msg "only owner"} old(msg.sender == owner());
    function setVestingPeriod(uint256 _vestingPeriod) public onlyOwner {
        require(_vestingPeriod > 0, "VestedAkro: vestingPeriod should be > 0");
        vestingPeriod = _vestingPeriod;
    }

    /**
     * @notice Sets vesting start date (as unix timestamp). Owner only
     * @param _vestingStart Unix timestamp.
     * if_succeeds {:msg "VestedAkro: vestingStart should be > 0"} _vestingStart > 0;
     * if_succeeds {:msg "only owner"} old(msg.sender == owner());
     */
    function setVestingStart(uint256 _vestingStart) public onlyOwner {
        require(_vestingStart > 0, "VestedAkro: vestingStart should be > 0");
        vestingStart = _vestingStart;
    }

    /**
     * @notice Sets vesting start date (as unix timestamp). Owner only
     * @param _vestingCliff Cliff in seconds (1 month by default)
     * if_succeeds {:msg "only owner"} old(msg.sender == owner());
     */
    function setVestingCliff(uint256 _vestingCliff) public onlyOwner {
        vestingCliff = _vestingCliff;
    }

    /// if_succeeds {:msg "only minter"} old(isMinter(msg.sender));
    function mint(address beneficiary, uint256 amount) public onlyMinter {
        totalSupply = totalSupply.add(amount);
        holders[beneficiary].unlocked = holders[beneficiary].unlocked.add(amount);
        emit Transfer(address(0), beneficiary, amount);
    }

    /**
     * @notice Adds AKRO liquidity to the swap contract
     * @param _amount Amout of AKRO added to the contract.
     * if_succeeds {:msg "only minter"} old(isMinter(msg.sender));
     */
    function addAkroLiquidity(uint256 _amount) public onlyMinter {
        require(_amount > 0, "Incorrect amount");
        
        IERC20Upgradeable(akro).safeTransferFrom(_msgSender(), address(this), _amount);
        
        emit AkroAdded(_amount);
    }

    /**
     * @notice Unlocks all avilable vAKRO for a holder
     * @param holder Whose funds to unlock
     * @return total unlocked amount awailable for redeem
     * if_succeeds {:msg "wrong holder"} holder != address(0);
     */
    function unlockAvailable(address holder) public returns(uint256) {
        require(holders[holder].batches.length > 0, "VestedAkro: nothing to unlock");
        claimAllFromBatches(holder);
        return holders[holder].unlocked;
    }

    /**
     * @notice Unlock all available vAKRO and redeem it
     * @return Amount redeemed
     */
    function unlockAndRedeemAll() public returns(uint256){
        address beneficiary = _msgSender();
        claimAllFromBatches(beneficiary);
        return redeemAllUnlocked();
    }

    /**
     * @notice Redeem all already unlocked vAKRO
     * @return Amount redeemed
     * if_succeeds {:msg "have unlocked"} holders[_msgSender()].unlocked == 0;
     */
    function redeemAllUnlocked() public returns(uint256){
        address beneficiary = _msgSender();
        require(!isSender(beneficiary), "VestedAkro: VestedAkroSender is not allowed to redeem");
        uint256 amount = holders[beneficiary].unlocked;
        if(amount == 0) return 0;
        require(akro.balanceOf(address(this)) >= amount, "Not enough AKRO");

        holders[beneficiary].unlocked = 0;
        totalSupply = totalSupply.sub(amount);
        akro.transfer(beneficiary, amount);
        emit Transfer(beneficiary, address(0), amount);
        return amount;
    }

    function balanceOf(address account) public override view returns (uint256) {
        Balance storage b = holders[account];
        return b.locked.add(b.unlocked);
    }

    function balanceInfoOf(address account) public view returns(uint256 locked, uint256 unlocked, uint256 unlockable) {
        Balance storage b = holders[account];
        return (b.locked, b.unlocked, calculateClaimableFromBatches(account));
    }

    function batchesInfoOf(address account) public view returns(uint256 firstUnclaimedBatch, uint256 totalBatches) {
        Balance storage b = holders[account];
        return (b.firstUnclaimedBatch, b.batches.length);
    }

    function batchInfo(address account, uint256 batch) public view 
    returns(uint256 amount, uint256 start, uint256 end, uint256 claimed, uint256 claimable) {
        VestedBatch storage vb = holders[account].batches[batch];
        (claimable,) = calculateClaimableFromBatch(vb);
        return (vb.amount, vb.start, vb.end, vb.claimed, claimable);
    }

    /// if_succeeds {:msg "wrong owner"} owner != address(0);
    /// if_succeeds {:msg "wrong spender"} spender != address(0);
    function _approve(address owner, address spender, uint256 amount) internal {
        require(owner != address(0), "VestedAkro: approve from the zero address");
        require(spender != address(0), "VestedAkro: approve to the zero address");

        allowances[owner][spender] = amount;
        emit Approval(owner, spender, amount);
    }

    /// if_succeeds {:msg "wrong spender"} sender != address(0);
    /// if_succeeds {:msg "wrong recipient"} recipient != address(0) || sender != recipient;
    /// if_succeeds {:msg "wrong amount"} amount > 0;
    /// if_succeeds {:msg "wrong transfer"} old(balanceOf(sender) - amount) == balanceOf(sender);
    /// if_succeeds {:msg "wrong transfer"} old(balanceOf(recipient) + amount) == balanceOf(recipient);
    /// if_succeeds {:msg "wrong transfer"} old(balanceOf(sender) + balanceOf(recipient)) == balanceOf(sender) + balanceOf(recipient);
    function _transfer(address sender, address recipient, uint256 amount) internal {
        require(sender != address(0), "VestedAkro: transfer from the zero address");
        require(recipient != address(0), "VestedAkro: transfer to the zero address");

        holders[sender].unlocked = holders[sender].unlocked.sub(amount, "VestedAkro: transfer amount exceeds unlocked balance");
        createOrModifyBatch(recipient, amount);

        emit Transfer(sender, recipient, amount);
    }

    /// if_succeeds {:msg "not locked"} old(holders[holder].locked + amount) == holders[holder].locked;
    function createOrModifyBatch(address holder, uint256 amount) internal {
        Balance storage b = holders[holder];

        if (b.batches.length == 0 || b.firstUnclaimedBatch == b.batches.length) {
            b.batches.push(VestedBatch({
                amount: amount,
                start: vestingStart,
                end: vestingStart.add(vestingPeriod),
                claimed: 0
            }));
        }
        else {
            uint256 batchAmount = b.batches[b.firstUnclaimedBatch].amount;
            b.batches[b.firstUnclaimedBatch].amount = batchAmount.add(amount);
        }
        b.locked = b.locked.add(amount);
        emit Locked(holder, amount);
    }

    function claimAllFromBatches(address holder) internal {
        claimAllFromBatches(holder, holders[holder].batches.length);
    }

    /// if_succeeds {:msg "wrong holder"} holder != address(0);
    /// if_succeeds {:msg "wrong calculation"} old(holders[holder].locked) - holders[holder].locked == holders[holder].unlocked - old(holders[holder].unlocked);
    function claimAllFromBatches(address holder, uint256 tillBatch) internal {
        Balance storage b = holders[holder];
        bool firstUnclaimedFound;
        uint256 claiming;
        for(uint256 i = b.firstUnclaimedBatch; i < tillBatch; i++) {
            (uint256 claimable, bool fullyClaimable) = calculateClaimableFromBatch(b.batches[i]);
            if(claimable > 0) {
                b.batches[i].claimed = b.batches[i].claimed.add(claimable);
                claiming = claiming.add(claimable);
            }
            if(!fullyClaimable && !firstUnclaimedFound) {
                b.firstUnclaimedBatch = i;
                firstUnclaimedFound = true;
            }
        }
        if(!firstUnclaimedFound) {
            b.firstUnclaimedBatch = b.batches.length;
        }
        if(claiming > 0){
            b.locked = b.locked.sub(claiming);
            b.unlocked = b.unlocked.add(claiming);
            emit Unlocked(holder, claiming);
        }
    }

    /**
     * @notice Calculates claimable amount from all batches
     * @param holder pointer to a batch
     * @return claimable amount
     */
    function calculateClaimableFromBatches(address holder) internal view returns(uint256) {
        Balance storage b = holders[holder];
        uint256 claiming;
        for(uint256 i = b.firstUnclaimedBatch; i < b.batches.length; i++) {
            (uint256 claimable,) = calculateClaimableFromBatch(b.batches[i]);
            claiming = claiming.add(claimable);
        }
        return claiming;
    }

    /**
     * @notice Calculates one batch
     * @param vb pointer to a batch
     * @return claimable amount and bool which is true if batch is fully claimable
     */
    function calculateClaimableFromBatch(VestedBatch storage vb) internal view returns(uint256, bool) {
        if (now < vb.start.add(vestingCliff) ) {
            return (0, false); // No unlcoks before cliff period is over
        }
        if(now >= vb.end) {
            return (vb.amount.sub(vb.claimed), true);
        }
        uint256 claimable = (vb.amount.mul(now.sub(vb.start)).div(vb.end.sub(vb.start))).sub(vb.claimed);
        return (claimable, false);
    }
}