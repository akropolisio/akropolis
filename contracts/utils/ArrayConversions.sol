// SPDX-License-Identifier: AGPL V3.0

pragma solidity >=0.6.0 <0.8.0;

library ArrayConversions {

    function convertUint256Array3(uint256[] memory values) internal returns(uint256[3] memory result) {
        result = [uint256(0), uint256(0), uint256(0)];
        for(uint256 i=0; i < 3; i++){
            result[i] = values[i];
        }
    }

    function convertUint256Array4(uint256[] memory values) internal returns(uint256[4] memory result) {
        result = [uint256(0), uint256(0), uint256(0), uint256(0)];
        for(uint256 i=0; i < 4; i++){
            result[i] = values[i];
        }
    }

}