// SPDX-License-Identifier: AGPL V3.0

pragma solidity >=0.6.0 <0.8.0;

pragma experimental ABIEncoderV2;

//solhint-disable func-order
interface IIndicesSavings {

    event IndexRegistered(address indexed lpIndex, address indexed lpRouter);
    event IndexActivated(address indexed lpIndex, address indexed lpRouter);
    event IndexDisabled(address indexed lpIndex);

    event Buy(
        address indexed lpIndex,
        uint256 indexed lpAmount,
        address indexed user,
        address token,
        uint256 tokenAmount
    );
    event Sell(
        address indexed lpIndex,
        uint256 indexed lpAmount,
        address indexed user,
        address token,
        uint256 tokenAmount
    );

    function buy(
        address _lpIndex,
        address _tokenIn,
        uint256 _amountIn,
        uint256 _amountOutMin,
        address[] calldata _path
    ) external payable;

    function sell(
        address _lpIndex,
        address _tokenOut,
        uint256 _amountIn,
        uint256 _amountOutMin,
        address[] calldata _path
    ) external;

    function buy(
        address[] calldata _lpIndices,
        address[] calldata _tokensIn,
        uint256[] calldata _amountsIn,
        uint256[] calldata _amountsOutMin,
        address[][] calldata _paths
    ) external payable;

    function sell(
        address[] calldata _lpIndices,
        address[] calldata _tokensOut,
        uint256[] calldata _amountsIn,
        uint256[] calldata _amountsOutMin,
        address[][] calldata _paths
    ) external payable;

    function registerIndex(address _lpIndex, address _lpRouter) external;

    function activateIndex(address _lpIndex, address _lpRouter) external;

    function deactivateIndex(address _lpIndex) external;

    function isIndexRegistered(address _lpIndex) external view returns (bool);

    function isIndexActive(address _lpIndex) external view returns (bool);

    function supportedIndices() external view returns (address[] memory);

    function activeIndices() external view returns (address[] memory);

    function getRouterForIndex(address _lpIndex) external view returns (address);
}