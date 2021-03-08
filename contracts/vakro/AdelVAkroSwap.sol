 
// SPDX-License-Identifier: AGPL V3.0
pragma solidity ^0.6.12;

import "@ozUpgradesV3/contracts/access/OwnableUpgradeable.sol";
import "@ozUpgradesV3/contracts/token/ERC20/IERC20Upgradeable.sol";
import "@ozUpgradesV3/contracts/token/ERC20/SafeERC20Upgradeable.sol";
import "@ozUpgradesV3/contracts/math/SafeMathUpgradeable.sol";
import "@ozUpgradesV3/contracts/utils/ReentrancyGuardUpgradeable.sol";
import "@ozUpgradesV3/contracts/cryptography/MerkleProofUpgradeable.sol";

import "../../interfaces/IERC20Burnable.sol";
import "../../interfaces/IERC20Mintable.sol";
import "../../interfaces/delphi/IStakingPool.sol";

contract AdelVAkroSwap is OwnableUpgradeable, ReentrancyGuardUpgradeable {
    using SafeERC20Upgradeable for IERC20Upgradeable;
    using SafeMathUpgradeable for uint256;
 
    event AdelSwapped(address indexed receiver, uint256 adelAmount, uint256 akroAmount);

    enum AdelSource{ WALLET, STAKE, REWARDS }

    //Addresses of affected contracts
    address public akro;
    address public adel;
    address public vakro;
    address public stakingPool;
    address public rewardAkroPool;
    address public rewardAdelPool;

    //Swap settings
    uint256 public minAmountToSwap = 0;
    uint256 public swapRateNumerator = 0;   //Amount of vAkro for 1 ADEL - 0 by default
    uint256 public swapRateDenominator = 1; //Akro amount = Adel amount * swapRateNumerator / swapRateDenominator
                                            //1 Adel = swapRateNumerator/swapRateDenominator Akro

    bytes32[] public merkleRoots;
    mapping (address => uint256[3]) public swappedAdel;

    bytes32[] public merkleRootsRewards;
    bytes32[] public merkleRootsRewardsVested;
    mapping (address => uint256[2]) public swappedAdelRewards;

    enum AdelRewardsSource{ WALLET, VESTED }

    modifier swapEnabled() {
        require(swapRateNumerator != 0, "Swap is disabled");
        _;
    }

    modifier enoughAdel(uint256 _adelAmount) {
        require(_adelAmount > 0 && _adelAmount >= minAmountToSwap, "Insufficient ADEL amount");
        _;
    }

    function initialize(address _akro, address _adel, address _vakro) virtual public initializer {
        require(_akro != address(0), "Zero address");
        require(_adel != address(0), "Zero address");
        require(_vakro != address(0), "Zero address");

        __Ownable_init();

        akro = _akro;
        adel = _adel;
        vakro = _vakro;
    }    

    //Setters for the swap tuning

    /**
     * @notice Sets the ADEL staking pool address
     * @param _stakingPool Adel staking pool address)
     */
    function setStakingPool(address _stakingPool) external onlyOwner {
        require(_stakingPool != address(0), "Zero address");
        stakingPool = _stakingPool;
    }

    /**
     * @notice Sets the staking pool addresses with ADEL rewards
     * @param _rewardAkroPool Akro staking pool address)
     * @param _rewardAdelPool Adel staking pool address)
     */
    function setRewardStakingPool(address _rewardAkroPool, address _rewardAdelPool) external onlyOwner {
        require(_rewardAkroPool != address(0) || _rewardAdelPool != address(0), "Zero address");
        rewardAkroPool = _rewardAkroPool;
        rewardAdelPool = _rewardAdelPool;
    }

    /**
     * @notice Sets the minimum amount of ADEL which can be swapped. 0 by default
     * @param _minAmount Minimum amount in wei (the least decimals)
     */
    function setMinSwapAmount(uint256 _minAmount) external onlyOwner {
        minAmountToSwap = _minAmount;
    }

    /**
     * @notice Sets the rate of ADEL to vAKRO swap: 1 ADEL = _swapRateNumerator/_swapRateDenominator vAKRO
     * @notice By default is set to 0, that means that swap is disabled
     * @param _swapRateNumerator Numerator for Adel converting. Can be set to 0 - that stops the swap.
     * @param _swapRateDenominator Denominator for Adel converting. Can't be set to 0
     */
    function setSwapRate(uint256 _swapRateNumerator, uint256 _swapRateDenominator) external onlyOwner {
        require(_swapRateDenominator > 0, "Incorrect value");
        swapRateNumerator = _swapRateNumerator;
        swapRateDenominator = _swapRateDenominator;
    }

    /**
     * @notice Sets the Merkle roots
     * @param _merkleRoots Array of hashes
     */
    function setMerkleRoots(bytes32[] memory _merkleRoots) external onlyOwner {
        require(_merkleRoots.length > 0, "Incorrect data");
        if (merkleRoots.length > 0) {
            delete merkleRoots;
        }
        merkleRoots = new bytes32[](_merkleRoots.length);
        merkleRoots = _merkleRoots;
    }

    /**
     * @notice Sets the Merkle roots for the rewards (on wallet)
     * @param _merkleRootsRewards Array of hashes for on-wallet rewards
     */
    function setMerkleRewardsRoots(bytes32[] memory _merkleRootsRewards) external onlyOwner {
        require(_merkleRootsRewards.length > 0, "Incorrect data");
        
        if (merkleRootsRewards.length > 0) {
            delete merkleRootsRewards;
        }
        merkleRootsRewards = new bytes32[](_merkleRootsRewards.length);
        merkleRootsRewards = _merkleRootsRewards;
    }

    /**
     * @notice Sets the Merkle roots for the rewards (vested)
     * @param _merkleRootsRewardsVested Array of hashes for vested rewards
     */
    function setMerkleVestedRewardsRoots(bytes32[] memory _merkleRootsRewardsVested) external onlyOwner {
        require(_merkleRootsRewardsVested.length > 0, "Incorrect data");
        
        if (merkleRootsRewardsVested.length > 0) {
            delete merkleRootsRewardsVested;
        }

        merkleRootsRewardsVested = new bytes32[](_merkleRootsRewardsVested.length);
        merkleRootsRewardsVested = _merkleRootsRewardsVested;
    }

    /**
     * @notice Withdraws all ADEL collected on a Swap contract
     * @param _recepient Recepient of ADEL.
     */
    function withdrawAdel(address _recepient) external onlyOwner {
        require(_recepient != address(0), "Zero address");
        uint256 _adelAmount = IERC20Upgradeable(adel).balanceOf(address(this));
        require(_adelAmount > 0, "Nothing to withdraw");
        IERC20Upgradeable(adel).safeTransfer(_recepient, _adelAmount);
    }

    /**
     * @notice Allows to swap ADEL token from the wallet for vAKRO
     * @param _adelAmount Amout of ADEL the user approves for the swap.
     * @param merkleRootIndex Index of a merkle root to be used for calculations
     * @param adelAllowedToSwap Maximum ADEL allowed for a user to swap
     * @param merkleProofs Array of consiquent merkle hashes
     */
    function swapFromAdel(
        uint256 _adelAmount,
        uint256 merkleRootIndex, 
        uint256 adelAllowedToSwap,
        bytes32[] memory merkleProofs
    ) 
        external nonReentrant swapEnabled enoughAdel(_adelAmount)
    {
        require(verifyMerkleProofs(_msgSender(), merkleRootIndex, adelAllowedToSwap, merkleProofs), "Merkle proofs not verified");

        IERC20Upgradeable(adel).safeTransferFrom(_msgSender(), address(this), _adelAmount);

        swap(_adelAmount, adelAllowedToSwap, AdelSource.WALLET);
    }
    

    /**
     * @notice Allows to swap ADEL token which is currently staked in StakingPool
     * @param merkleRootIndex Index of a merkle root to be used for calculations
     * @param adelAllowedToSwap Maximum ADEL allowed for a user to swap
     * @param merkleProofs Array of consiquent merkle hashes
     */
    function swapFromStakedAdel(
        uint256 merkleRootIndex, 
        uint256 adelAllowedToSwap,
        bytes32[] memory merkleProofs
    )
        external nonReentrant swapEnabled
    {
        require(stakingPool != address(0), "Swap from stake is disabled");

        require(verifyMerkleProofs(_msgSender(), merkleRootIndex, adelAllowedToSwap, merkleProofs), "Merkle proofs not verified");
        
        uint256 adelBefore = IERC20Upgradeable(adel).balanceOf(address(this));
        uint256 akroBefore = IERC20Upgradeable(akro).balanceOf(address(this));
        uint256 _adelAmount = IStakingPool(stakingPool).withdrawStakeForSwap(_msgSender(), adel, "0x");
        uint256 adelAfter = IERC20Upgradeable(adel).balanceOf(address(this));
        uint256 akroAfter = IERC20Upgradeable(akro).balanceOf(address(this));
        
        require( adelAfter - adelBefore == _adelAmount, "ADEL was not transferred");

        if (akroAfter - akroBefore > 0) {
            IERC20Upgradeable(akro).safeTransfer(_msgSender(), akroAfter - akroBefore);
        }
                
        swap(_adelAmount, adelAllowedToSwap, AdelSource.STAKE);
    }


    /**
     * @notice Allows to swap ADEL token which belongs to vested unclaimed rewards
     * @param merkleRootIndex Index of a merkle root to be used for calculations
     * @param adelAllowedToSwap Maximum ADEL allowed for a user to swap
     * @param merkleProofs Array of consiquent merkle hashes
     */
    function swapFromRewardAdel(
        uint256 merkleRootIndex, 
        uint256 adelAllowedToSwap,
        bytes32[] memory merkleProofs
    ) 
        external nonReentrant swapEnabled
    {
        require(rewardAkroPool != address(0) || rewardAdelPool != address(0), "Swap from rewards is disabled");

        require(verifyMerkleProofs(_msgSender(), merkleRootIndex, adelAllowedToSwap, merkleProofs), "Merkle proofs not verified");

        uint256 adelBefore;
        uint256 _adelAmount;
        uint256 adelAfter;
        uint256 adelReceived;

        //Withdraw ADEL rewards from AKRO staking pool
        if (rewardAkroPool != address(0))
        {
            adelBefore = IERC20Upgradeable(adel).balanceOf(address(this));
            _adelAmount = IStakingPool(rewardAkroPool).withdrawRewardForSwap(_msgSender(), adel);
            adelAfter = IERC20Upgradeable(adel).balanceOf(address(this));

            require( adelAfter - adelBefore == _adelAmount, "ADEL was not transferred from AKRO pool");

            adelReceived = adelReceived.add(_adelAmount);
        }

        //Withdraw ADEL rewards from ADEL staking pool
        if (rewardAdelPool != address(0))
        {
            adelBefore = IERC20Upgradeable(adel).balanceOf(address(this));
            _adelAmount = IStakingPool(rewardAdelPool).withdrawRewardForSwap(_msgSender(), adel);
            adelAfter = IERC20Upgradeable(adel).balanceOf(address(this));

            require( adelAfter - adelBefore == _adelAmount, "ADEL was not transferred rom ADEL pool");

            adelReceived = adelReceived.add(_adelAmount);
        }
        
        swap(adelReceived, adelAllowedToSwap, AdelSource.REWARDS);
    }

    /**
     * @notice Allows to swap ADEL token from vesting rewards from the wallet for vAKRO
     * @param _adelAmount Amout of ADEL vested rewards the user approves for the swap.
     * @param merkleRootIndex Index of a merkle root to be used for calculations
     * @param adelAllowedToSwap Maximum ADEL allowed for a user to swap
     * @param merkleProofs Array of consiquent merkle hashes
     */
    function swapFromAdelWalletRewards(
        uint256 _adelAmount,
        uint256 merkleRootIndex, 
        uint256 adelAllowedToSwap,
        bytes32[] memory merkleProofs
    ) 
        external nonReentrant swapEnabled enoughAdel(_adelAmount)
    {
        require(verifyRewardsMerkleProofs(_msgSender(), merkleRootIndex, adelAllowedToSwap, merkleProofs), "Merkle proofs not verified");

        IERC20Upgradeable(adel).safeTransferFrom(_msgSender(), address(this), _adelAmount);

        swapRewards(_adelAmount, adelAllowedToSwap, AdelRewardsSource.WALLET);
    }

    /**
     * @notice Allows to swap ADEL token from not sent vested rewards
     * @param _adelAmount Amout of ADEL vested rewards the user approves for the swap.
     * @param merkleRootIndex Index of a merkle root to be used for calculations
     * @param adelAllowedToSwap Maximum ADEL allowed for a user to swap
     * @param merkleProofs Array of consiquent merkle hashes
     */
    function swapFromAdelVestedRewards(
        uint256 _adelAmount,
        uint256 merkleRootIndex, 
        uint256 adelAllowedToSwap,
        bytes32[] memory merkleProofs
    ) 
        external nonReentrant swapEnabled
    {
        require(verifyVestedRewardsMerkleProofs(_msgSender(), merkleRootIndex, adelAllowedToSwap, merkleProofs), "Merkle proofs not verified");

        // No ADEL transfers here

        swapRewards(_adelAmount, adelAllowedToSwap, AdelRewardsSource.VESTED);
    }

    /**
     * @notice Verifies merkle proofs of user to be elligible for swap
     * @param _account Address of a user
     * @param _merkleRootIndex Index of a merkle root to be used for calculations
     * @param _adelAllowedToSwap Maximum ADEL allowed for a user to swap
     * @param _merkleProofs Array of consiquent merkle hashes
     */
    function verifyMerkleProofs(
        address _account,
        uint256 _merkleRootIndex,
        uint256 _adelAllowedToSwap,
        bytes32[] memory _merkleProofs) virtual public view returns(bool)
    {
        require(_merkleProofs.length > 0, "No Merkle proofs");
        require(_merkleRootIndex < merkleRoots.length, "Merkle roots are not set");

        bytes32 node = keccak256(abi.encodePacked(_account, _adelAllowedToSwap));
        return MerkleProofUpgradeable.verify(_merkleProofs, merkleRoots[_merkleRootIndex], node);
    }

    /**
     * @notice Verifies rewards merkle proofs of user to be elligible for swap
     * @param _account Address of a user
     * @param _merkleRootIndex Index of a merkle root to be used for calculations
     * @param _adelAllowedToSwap Maximum ADEL allowed for a user to swap
     * @param _merkleProofs Array of consiquent merkle hashes
     */
    function verifyRewardsMerkleProofs(
        address _account,
        uint256 _merkleRootIndex,
        uint256 _adelAllowedToSwap,
        bytes32[] memory _merkleProofs) virtual public view returns(bool)
    {
        require(_merkleProofs.length > 0, "No Merkle proofs");
        require(_merkleRootIndex < merkleRootsRewards.length, "Merkle roots are not set");

        bytes32 node = keccak256(abi.encodePacked(_account, _adelAllowedToSwap));
        return MerkleProofUpgradeable.verify(_merkleProofs, merkleRootsRewards[_merkleRootIndex], node);
    }

    /**
     * @notice Verifies vested rewards merkle proofs of user to be elligible for swap
     * @param _account Address of a user
     * @param _merkleRootIndex Index of a merkle root to be used for calculations
     * @param _adelAllowedToSwap Maximum ADEL allowed for a user to swap
     * @param _merkleProofs Array of consiquent merkle hashes
     */
    function verifyVestedRewardsMerkleProofs(
        address _account,
        uint256 _merkleRootIndex,
        uint256 _adelAllowedToSwap,
        bytes32[] memory _merkleProofs) virtual public view returns(bool)
    {
        require(_merkleProofs.length > 0, "No Merkle proofs");
        require(_merkleRootIndex < merkleRootsRewardsVested.length, "Merkle roots are not set");

        bytes32 node = keccak256(abi.encodePacked(_account, _adelAllowedToSwap));
        return MerkleProofUpgradeable.verify(_merkleProofs, merkleRootsRewardsVested[_merkleRootIndex], node);
    }

    /**merkleRoots
     * @notice Returns the actual amount of ADEL swapped by a user
     * @param _account Address of a user
     */
    function adelSwapped(address _account) public view returns (uint256)
    {
        return swappedAdel[_account][0] + swappedAdel[_account][1] + swappedAdel[_account][2];
    }

    /**
     * @notice Returns the actual amount of ADEL vesting rewards swapped by a user
     * @param _account Address of a user
     */
    function adelRewardsSwapped(address _account) public view returns (uint256)
    {
        return swappedAdelRewards[_account][0] + swappedAdelRewards[_account][1];
    }

    /**
     * @notice Internal function to collect ADEL and mint vAkro for the sender
     * @notice Function lays on the fact, that ADEL is already on the contract
     * @param _adelAmount Amout of ADEL the contract needs to swap.
     * @param _adelAllowedToSwap Maximum ADEL from any source allowed to swap for user.
     *                           Any extra ADEL which exceeds this value is sent to the user
     * @param _index Number of the source of ADEL (wallet, stake, rewards)
     */
    function swap(uint256 _adelAmount, uint256 _adelAllowedToSwap, AdelSource _index) internal
    {
        uint256 amountSwapped = adelSwapped(_msgSender());
        require(amountSwapped < _adelAllowedToSwap, "Limit for swap is reached");
        require(_adelAmount != 0 && _adelAmount >= minAmountToSwap, "Not enough ADEL");

        uint256 actualAdelAmount;
        uint256 adelChange;
        if (amountSwapped.add(_adelAmount) > _adelAllowedToSwap) {
            actualAdelAmount = _adelAllowedToSwap.sub(amountSwapped);
            adelChange = _adelAmount.sub(actualAdelAmount);
        }
        else {
            actualAdelAmount = _adelAmount;
        }

        uint256 vAkroAmount = actualAdelAmount.mul(swapRateNumerator).div(swapRateDenominator);

        swappedAdel[_msgSender()][uint128(_index)] = swappedAdel[_msgSender()][uint128(_index)].add(actualAdelAmount);
        IERC20Mintable(vakro).mint(address(this), vAkroAmount);
        IERC20Upgradeable(vakro).transfer(_msgSender(), vAkroAmount);

        emit AdelSwapped(_msgSender(), actualAdelAmount, vAkroAmount);

        if (adelChange > 0)
            IERC20Upgradeable(adel).safeTransfer(_msgSender(), adelChange);
    }

    /**
     * @notice Internal function to mint vAkro for ADEL from vesting rewards
     * @notice Function lays on the fact, that ADEL is already on the contract
     * @param _adelAmount Amout of ADEL the contract needs to swap.
     * @param _adelAllowedToSwap Maximum ADEL vested rewards from any source allowed to swap for user.
     *                           Any extra ADEL which exceeds this value is sent to the user
     * @param _index Number of the source of vested rewards ADEL (wallet, vested unlock)
     */
    function swapRewards(uint256 _adelAmount, uint256 _adelAllowedToSwap, AdelRewardsSource _index) internal
    {
        uint256 newAmount = swappedAdelRewards[_msgSender()][uint128(_index)].add(_adelAmount);

        require( newAmount <= _adelAllowedToSwap, "Limit exceeded");
        require(_adelAmount != 0 && _adelAmount >= minAmountToSwap, "Not enough ADEL");

        uint256 vAkroAmount = _adelAmount.mul(swapRateNumerator).div(swapRateDenominator);
        
        swappedAdelRewards[_msgSender()][uint128(_index)] = newAmount;
        IERC20Mintable(vakro).mint(address(this), vAkroAmount);
        IERC20Upgradeable(vakro).transfer(_msgSender(), vAkroAmount);

        emit AdelSwapped(_msgSender(), _adelAmount, vAkroAmount);
    }
}