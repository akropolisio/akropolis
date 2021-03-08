 
// SPDX-License-Identifier: AGPL V3.0
pragma solidity ^0.6.12;

import "../vakro/AdelVAkroSwap.sol";
import "../../interfaces/IERC20Mintable.sol";
import "../../interfaces/delphi/IStakingPool.sol";

contract TestAdelVAkroSwap is AdelVAkroSwap {
    function initialize(address _akro, address _adel, address _vakro) public override initializer {
        AdelVAkroSwap.initialize(_akro, _adel, _vakro);
    }    

    function verifyMerkleProofs(
        address _account,
        uint256 _merkleRootIndex,
        uint256 _adelAllowedToSwap,
        bytes32[] memory _merkleProofs) public override view returns(bool)
    {
        return true;
    }

    function verifyRewardsMerkleProofs(
        address _account,
        uint256 _merkleRootIndex,
        uint256 _adelAllowedToSwap,
        bytes32[] memory _merkleProofs) public override view returns(bool)
    {
        return true;
    }

    function verifyVestedRewardsMerkleProofs(
        address _account,
        uint256 _merkleRootIndex,
        uint256 _adelAllowedToSwap,
        bytes32[] memory _merkleProofs) public override view returns(bool)
    {
        return true;
    }
}