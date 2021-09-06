"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.constants = void 0;
const utils_1 = require("@0x/utils");
const web3_wrapper_1 = require("@0x/web3-wrapper");
const ethUtil = require("ethereumjs-util");
const _ = require("lodash");
const types_1 = require("./types");
const TESTRPC_PRIVATE_KEYS_STRINGS = [
    '0xf2f48ee19680706196e2e339e5da3491186e0c4c5030670656b0e0164837257d',
    '0x5d862464fe9303452126c8bc94274b8c5f9874cbd219789b3eb2128075a76f72',
    '0xdf02719c4df8b9b8ac7f551fcb5d9ef48fa27eef7a66453879f4d8fdc6e78fb1',
    '0xff12e391b79415e941a94de3bf3a9aee577aed0731e297d5cfa0b8a1e02fa1d0',
    '0x752dd9cf65e68cfaba7d60225cbdbc1f4729dd5e5507def72815ed0d8abc6249',
    '0xefb595a0178eb79a8df953f87c5148402a224cdf725e88c0146727c6aceadccd',
    '0x83c6d2cc5ddcf9711a6d59b417dc20eb48afd58d45290099e5987e3d768f328f',
    '0xbb2d3f7c9583780a7d3904a2f55d792707c345f21de1bacb2d389934d82796b2',
    '0xb2fd4d29c1390b71b8795ae81196bfd60293adf99f9d32a0aff06288fcdac55f',
    '0x23cb7121166b9a2f93ae0b7c05bde02eae50d64449b2cbb42bc84e9d38d6cc89',
    '0x5ad34d7f8704ed33ab9e8dc30a76a8c48060649204c1f7b21b973235bba8092f',
    '0xf18b03c1ae8e3876d76f20c7a5127a169dd6108c55fe9ce78bc7a91aca67dee3',
    '0x4ccc4e7d7843e0701295e8fd671332a0e2f1e92d0dab16e8792e91cb0b719c9d',
    '0xd7638ae813450e710e6f1b09921cc1593181073ce2099fb418fc03a933c7f41f',
    '0xbc7bbca8ca15eb567be60df82e4452b13072dcb60db89747e3c85df63d8270ca',
    '0x55131517839bf782e6e573bc3ac8f262efd2b6cb0ac86e8f147db26fcbdb15a5',
    '0x6c2b5a16e327e0c4e7fafca5ae35616141de81f77da66ee0857bc3101d446e68',
    '0xfd79b71625eec963e6ec42e9b5b10602c938dfec29cbbc7d17a492dd4f403859',
    '0x3003eace3d4997c52ba69c2ca97a6b5d0d1216d894035a97071590ee284c1023',
    '0x84a8bb71450a1b82be2b1cdd25d079cbf23dc8054e94c47ad14510aa967f45de',
];
const MAX_UINT256 = new utils_1.BigNumber(2).pow(256).minus(1);
exports.constants = {
    BASE_16: 16,
    INVALID_OPCODE: 'invalid opcode',
    TESTRPC_CHAIN_ID: 1337,
    // Note(albrow): In practice V8 and most other engines limit the minimum
    // interval for setInterval to 10ms. We still set it to 0 here in order to
    // ensure we always use the minimum interval.
    AWAIT_TRANSACTION_MINED_MS: 0,
    MAX_ETHERTOKEN_WITHDRAW_GAS: 43000,
    MAX_EXECUTE_TRANSACTION_GAS: 1000000,
    MAX_TOKEN_TRANSFERFROM_GAS: 80000,
    MAX_TOKEN_APPROVE_GAS: 60000,
    MAX_TRANSFER_FROM_GAS: 150000,
    MAX_MATCH_ORDERS_GAS: 400000,
    DUMMY_TOKEN_NAME: '',
    DUMMY_TOKEN_SYMBOL: '',
    DUMMY_TOKEN_DECIMALS: new utils_1.BigNumber(18),
    DUMMY_TOKEN_TOTAL_SUPPLY: new utils_1.BigNumber(0),
    NULL_BYTES: '0x',
    NUM_DUMMY_ERC20_TO_DEPLOY: 4,
    NUM_DUMMY_ERC721_TO_DEPLOY: 2,
    NUM_ERC721_TOKENS_TO_MINT: 4,
    NUM_DUMMY_ERC1155_CONTRACTS_TO_DEPLOY: 2,
    NUM_ERC1155_FUNGIBLE_TOKENS_MINT: 4,
    NUM_ERC1155_NONFUNGIBLE_TOKENS_MINT: 4,
    NULL_BYTES4: '0x00000000',
    NULL_ADDRESS: '0x0000000000000000000000000000000000000000',
    NULL_BYTES32: '0x0000000000000000000000000000000000000000000000000000000000000000',
    UNLIMITED_ALLOWANCE_IN_BASE_UNITS: MAX_UINT256,
    MAX_UINT256,
    MAX_UINT32: new utils_1.BigNumber(2).pow(32).minus(1),
    TESTRPC_PRIVATE_KEYS: _.map(TESTRPC_PRIVATE_KEYS_STRINGS, privateKeyString => ethUtil.toBuffer(privateKeyString)),
    INITIAL_ERC20_BALANCE: web3_wrapper_1.Web3Wrapper.toBaseUnitAmount(new utils_1.BigNumber(10000), 18),
    INITIAL_ERC20_ALLOWANCE: web3_wrapper_1.Web3Wrapper.toBaseUnitAmount(new utils_1.BigNumber(10000), 18),
    INITIAL_ERC1155_FUNGIBLE_BALANCE: web3_wrapper_1.Web3Wrapper.toBaseUnitAmount(new utils_1.BigNumber(10000), 18),
    INITIAL_ERC1155_FUNGIBLE_ALLOWANCE: web3_wrapper_1.Web3Wrapper.toBaseUnitAmount(new utils_1.BigNumber(10000), 18),
    STATIC_ORDER_PARAMS: {
        makerAssetAmount: web3_wrapper_1.Web3Wrapper.toBaseUnitAmount(new utils_1.BigNumber(100), 18),
        takerAssetAmount: web3_wrapper_1.Web3Wrapper.toBaseUnitAmount(new utils_1.BigNumber(200), 18),
        makerFee: web3_wrapper_1.Web3Wrapper.toBaseUnitAmount(new utils_1.BigNumber(1), 18),
        takerFee: web3_wrapper_1.Web3Wrapper.toBaseUnitAmount(new utils_1.BigNumber(1), 18),
    },
    WORD_LENGTH: 32,
    ADDRESS_LENGTH: 20,
    ZERO_AMOUNT: new utils_1.BigNumber(0),
    PERCENTAGE_DENOMINATOR: new utils_1.BigNumber(10).pow(18),
    TIME_BUFFER: new utils_1.BigNumber(1000),
    KECCAK256_NULL: ethUtil.bufferToHex(ethUtil.keccak256(Buffer.alloc(0))),
    MAX_UINT256_ROOT: new utils_1.BigNumber('340282366920938463463374607431768211456'),
    ONE_ETHER: new utils_1.BigNumber(1e18),
    EIP712_DOMAIN_NAME: '0x Protocol',
    EIP712_DOMAIN_VERSION: '3.0.0',
    DEFAULT_GAS_PRICE: 1,
    NUM_TEST_ACCOUNTS: 20,
    PPM_DENOMINATOR: 1e6,
    PPM_100_PERCENT: 1e6,
    MAX_CODE_SIZE: 24576,
    SINGLE_FILL_FN_NAMES: [types_1.ExchangeFunctionName.FillOrder, types_1.ExchangeFunctionName.FillOrKillOrder],
    BATCH_FILL_FN_NAMES: [
        types_1.ExchangeFunctionName.BatchFillOrders,
        types_1.ExchangeFunctionName.BatchFillOrKillOrders,
        types_1.ExchangeFunctionName.BatchFillOrdersNoThrow,
    ],
    MARKET_FILL_FN_NAMES: [
        types_1.ExchangeFunctionName.MarketBuyOrdersFillOrKill,
        types_1.ExchangeFunctionName.MarketSellOrdersFillOrKill,
        types_1.ExchangeFunctionName.MarketBuyOrdersNoThrow,
        types_1.ExchangeFunctionName.MarketSellOrdersNoThrow,
    ],
    MATCH_ORDER_FN_NAMES: [types_1.ExchangeFunctionName.MatchOrders, types_1.ExchangeFunctionName.MatchOrdersWithMaximalFill],
    BATCH_MATCH_ORDER_FN_NAMES: [
        types_1.ExchangeFunctionName.BatchMatchOrders,
        types_1.ExchangeFunctionName.BatchMatchOrdersWithMaximalFill,
    ],
    CANCEL_ORDER_FN_NAMES: [
        types_1.ExchangeFunctionName.CancelOrder,
        types_1.ExchangeFunctionName.BatchCancelOrders,
        types_1.ExchangeFunctionName.CancelOrdersUpTo,
    ],
};
//# sourceMappingURL=constants.js.map