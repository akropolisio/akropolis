import pytest
import brownie
from web3 import Web3
from hexbytes import HexBytes

ADEL_AKRO_RATE = 15


def get_users():
    users = (
        "0xc97ad401c75e6bfb5694899cd3271485d27c6ea4",  # User to swap from wallet
        "0xf42a339f93c1fa4c5d9ace33db308a504e7b0bde",  # User to swap from stake
        "0xb1f9a358003ae5145805e936db3af3c22368e324",  # User to swap from rewards (Adel staking)
        "0xa215f1b06e7945d331f2df30961027123947a40d",  # User to swap from both stake and rewards (Adel staking)
        "0x8efd9addd8de6a4e64664d1893dec51f8c3339e9",  # User to swap from wallet and stake to get change to the wallet
        "0x19870de096523b6eaed10da9fbeb82285451c7bd",  # User to swap from rewards (Adel and Akro stakings)
    )
    return users


def get_rewards_users():
    users = (
        "0x4dab9b8fca17a37e5ef0eef7d1ac09e2ac1580fb",  # User to swap from wallet
        "0x8e3fabf5a1e4b773c227d2646eb2470263d3a1bf",  # User to swap from vesting
    )
    return users


def users_proofs():
    users = get_users()
    proofs = [
        {
            "amount_wallet": 1036421477600000000000,
            "amount_stake": 0,
            "amount_rewards": 0,
            "rootIndex": 0,
            "maxAmount": 1036421477600000000000,
            "proofs": [
                HexBytes(
                    "0xf998860e2d92d57193e8083b5a10ea2a58e3de4a8a6166c936b868982c5ec6c5"
                ),
                HexBytes(
                    "0x95cddcd8fe4312ff02e412d4f1a0be2716053014d26bd70e11d363e79a2ba958"
                ),
                HexBytes(
                    "0x079d7ae5d25d5dfa25259faf9fe3941ceb2b0a893490825226b79dfa920f3c4e"
                ),
                HexBytes(
                    "0x875d4362ebaccfa1b902cdb5d83ba1955208a232823204a46aa40733bc579633"
                ),
                HexBytes(
                    "0x59670fe60a33184d3f6224b8911f9af72805185d718b1c936fca8ae17705c5b8"
                ),
                HexBytes(
                    "0x51ef94d740b3c815649161f2c1f4f81d118942748d7121ac264c355b792fd4de"
                ),
                HexBytes(
                    "0xdfac3ac3b255c15c3e887442081cfe319ed70fb9cc8ccc62bf33978d078af849"
                ),
            ],
        },
        {
            "amount_rewards_from_adel": 433118258131121660401,
            "amount_rewards_from_akro": 528096136280856926374,
            "amount_wallet": 1428909636600000000000,
            "amount_stake": 6260010000000000000000,
            "amount_rewards": 433118258131121660401 + 528096136280856926374,
            "rootIndex": 0,
            "maxAmount": 8650134031011978586775,
            "proofs": [
                HexBytes(
                    "0x0f960cae0771295455bace46e4aedb07245742c2cf613499798795e943c01bb9"
                ),
                HexBytes(
                    "0xe6af4da2a77655e80f9bd07c2b58fa94728cd5aee278711d8386751e995fae68"
                ),
                HexBytes(
                    "0x2533295b638307210ca1d5adc1094a546ca9593c787552326b36b86fddb92d8e"
                ),
                HexBytes(
                    "0x27d4be9f1c8b9c2398045ed357e2b51a46717b01c9977614dc66932c521aeab8"
                ),
                HexBytes(
                    "0x0a94e0fbf3a4f169b01ce7ca9c8927631c3836b1aa98199d56115ba59bd0885a"
                ),
                HexBytes(
                    "0xb4fb904424d5a825239d24d658ca5e506d30faa49d48c87003f721667afab28e"
                ),
                HexBytes(
                    "0xdfac3ac3b255c15c3e887442081cfe319ed70fb9cc8ccc62bf33978d078af849"
                ),
            ],
        },
        {
            "amount_wallet": 31481786698989648049,
            "amount_stake": 302885125819850880724,
            "amount_rewards": 3670344697071449027,
            "rootIndex": 0,
            "maxAmount": 338037257215911977800,
            "proofs": [
                HexBytes(
                    "0x2f38bdff1807dfb912295e05d915e5e30234eb9282c635edc44ae1f6cab38327"
                ),
                HexBytes(
                    "0xdae130919ffbe63bdc6ac438053987ed4877b9a304dc9bb94770dd6437b12bb8"
                ),
                HexBytes(
                    "0x314f80fa2fbffda0d3adae944c1fbd7d5fc5087327b5444015e28d1abf25f0ba"
                ),
                HexBytes(
                    "0x1a2e5a7d0ecb0d02601777d80643bfefe3ab0ef4087dbe82b0155befd19f4156"
                ),
                HexBytes(
                    "0x5eb88e4222b60f92cd3e512ec4b092b61f3769526b4d3d7a80c43df9b3572b96"
                ),
                HexBytes(
                    "0x51ef94d740b3c815649161f2c1f4f81d118942748d7121ac264c355b792fd4de"
                ),
                HexBytes(
                    "0xdfac3ac3b255c15c3e887442081cfe319ed70fb9cc8ccc62bf33978d078af849"
                ),
            ],
        },
        {
            "amount_wallet": 4130000000000000000,
            "amount_stake": 122202583170062799350,
            "amount_rewards": 8454965720780178145,
            "rootIndex": 0,
            "maxAmount": 134787548890842977495,
            "proofs": [
                HexBytes(
                    "0xb6967a2e899018c421adc71a0433590b09051a5ec02c10c6c9a268f7dcf1103c"
                ),
                HexBytes(
                    "0x587c24103fff0fa07849a8917193ed6b02a6a3d9e534531f90b73a0fdacac26e"
                ),
                HexBytes(
                    "0xe8243531c2b48bede9404bc63b735f79a494f392d6f8d75627a5995ac6fa640b"
                ),
                HexBytes(
                    "0x3c422af1c5ab9de36ce5eb4c8c0e0eeca9162cc2f6804754bbb336d57cf65dce"
                ),
                HexBytes(
                    "0x5eb88e4222b60f92cd3e512ec4b092b61f3769526b4d3d7a80c43df9b3572b96"
                ),
                HexBytes(
                    "0x51ef94d740b3c815649161f2c1f4f81d118942748d7121ac264c355b792fd4de"
                ),
                HexBytes(
                    "0xdfac3ac3b255c15c3e887442081cfe319ed70fb9cc8ccc62bf33978d078af849"
                ),
            ],
        },
        {
            "amount_wallet": 683108047500000000000,
            "amount_stake": 20424450350752168953589,
            "amount_rewards": 0,
            "rootIndex": 0,
            "maxAmount": 21107558398252168953589,
            "proofs": [
                HexBytes(
                    "0x446193ccfd7dc68e9f394f5e503f07c55647ad08306150cf9d5980954dd4fd69"
                ),
                HexBytes(
                    "0xbe25a70184c7817af7ddac562b6e2cd698ff4cf9e98fee99ca1fad046ca0496f"
                ),
                HexBytes(
                    "0x314f80fa2fbffda0d3adae944c1fbd7d5fc5087327b5444015e28d1abf25f0ba"
                ),
                HexBytes(
                    "0x1a2e5a7d0ecb0d02601777d80643bfefe3ab0ef4087dbe82b0155befd19f4156"
                ),
                HexBytes(
                    "0x5eb88e4222b60f92cd3e512ec4b092b61f3769526b4d3d7a80c43df9b3572b96"
                ),
                HexBytes(
                    "0x51ef94d740b3c815649161f2c1f4f81d118942748d7121ac264c355b792fd4de"
                ),
                HexBytes(
                    "0xdfac3ac3b255c15c3e887442081cfe319ed70fb9cc8ccc62bf33978d078af849"
                ),
            ],
        },
        {
            "amount_rewards_from_adel": 52292486004089295696,
            "amount_rewards_from_akro": 82950431239994386691,
            "amount_wallet": 61186896534522935481,
            "amount_stake": 1455160000000000000000,
            "amount_rewards": 52292486004089295696 + 82950431239994386691,
            "rootIndex": 0,
            "maxAmount": 1651589813778606617868,
            "proofs": [
                HexBytes(
                    "0x61684f6b59b4970cce1fd80eebd5d40f6e3d71f7b9dca891f6854b44e649a8a4"
                ),
                HexBytes(
                    "0xb509f4494d50fb73fc7976ad9298add618490fc9ea50d1e4bc41852606667e20"
                ),
                HexBytes(
                    "0x038cc62147df445322e4a1d783365dd76ac4ef0edc0a46fbf7ecba15d4b484b9"
                ),
                HexBytes(
                    "0x3c422af1c5ab9de36ce5eb4c8c0e0eeca9162cc2f6804754bbb336d57cf65dce"
                ),
                HexBytes(
                    "0x5eb88e4222b60f92cd3e512ec4b092b61f3769526b4d3d7a80c43df9b3572b96"
                ),
                HexBytes(
                    "0x51ef94d740b3c815649161f2c1f4f81d118942748d7121ac264c355b792fd4de"
                ),
                HexBytes(
                    "0xdfac3ac3b255c15c3e887442081cfe319ed70fb9cc8ccc62bf33978d078af849"
                ),
            ],
        },
    ]

    return dict(zip(users, proofs))


def users_rewards_proofs():
    users = get_rewards_users()
    proofs = [
        {
            "amount_wallet": 1784857882460904308966,
            "amount_vested": 0,
            "rootIndex": 0,
            "maxAmount": 1784857882460904308966,
            "proofs": [
                HexBytes(
                    "0x283e9304873f737cc0070f4aa0374ddb6d37704740b2c5695fb042f91dbfd5b4"
                ),
                HexBytes(
                    "0x5d9d33bba798327530e426e3189748fb4abde545b859a15ea2d9de93a05207f7"
                ),
                HexBytes(
                    "0x93542295dcb174d57c347ab1834c710433d935edf320e28f7cd4a5e30f235355"
                ),
                HexBytes(
                    "0xaf33adee34ddee891f2eadab44b4fee0d83ec897583b9b1519c9a6c4e014fc9b"
                ),
                HexBytes(
                    "0xafc383004bec08a6dee45f83e5b5d6f78875f5e6847d1c8e25035d1cde2df4d4"
                ),
                HexBytes(
                    "0x0cf8320a2647757f088ba0311d80bfb4087a937afb438e9a922c45e4585c58d4"
                ),
                HexBytes(
                    "0x22ca6b343d85019f532177d1577fb42fbfd06cb5da3be501e5b562f133fc5cbe"
                ),
            ],
        },
        {
            "amount_wallet": 979210059829455378873,
            "amount_vested": 4545815708308316933639,
            "rootIndex": 2,
            "rootIndexVested": 3,
            "maxAmount": 979210059829455378873,
            "maxAmountVested": 4545815708308316933639,
            "proofs": [
                HexBytes(
                    "0x81b2aff6231cd4c31ed2d439aa87b2dc9e29bb0bc6bcddf786a60ce8f148bd7e"
                ),
                HexBytes(
                    "0xf2b3dcbe7b1ad08f032c5edaf34e81f3bcf1a6a0408f0deaed711e3bfa5ce7f4"
                ),
                HexBytes(
                    "0x9c2b71e63e25bf1f047b0c1d731c296404c4bc1777eba41a64d263d351ecc4e3"
                ),
                HexBytes(
                    "0x1cc7f7adc1540bb9919c77a6ff3b22ac64c99ac02042bab6f46451a635366733"
                ),
                HexBytes(
                    "0xafe576cf2b75eff1926ff20ecde452dd57d6aebb606849089f389d5186d0f514"
                ),
                HexBytes(
                    "0x45077adeb439ca8c40644e165809362a9ef1e5ade663da928e184245e9308570"
                ),
                HexBytes(
                    "0x97966c42525421b737811d50148ca02800451a54dd268da2f04954eb997ec2df"
                ),
            ],
            "proofsVested": [
                HexBytes(
                    "0x9b9d0f72cef313828c4088fdbb549be17ea0c749e3a99f5e3d785f6706a39b86"
                ),
                HexBytes(
                    "0xa8dbce1cb2379f6ebec4307fe62769f38ec3be5f797ecd31069ab9f7c59bd0d4"
                ),
                HexBytes(
                    "0x54a9f3dceaa6cc7d34ba3f3b7111b1ceb906066bd8a3333009ef245c257213e6"
                ),
                HexBytes(
                    "0xce034c685c4dc9c3a86616ba12d1a4fa44ad557b4bc7ed9de05fc3b67e0cb368"
                ),
                HexBytes(
                    "0xe943c90f9699b1946eea23633a8a819f1e4a5c96611ddc356bc47a716c9d10af"
                ),
                HexBytes(
                    "0x8c666d62e7bbd178cb2357b1a96aeff7e20fc73218c7af5d06300a7f99647372"
                ),
                HexBytes(
                    "0x592811736d5e4e2b55e88db19d5a827c330253d6494ebe63a2b51638a9003700"
                ),
            ],
        },
    ]

    return dict(zip(users, proofs))


def merkle_roots():
    return [
        HexBytes("0x15a33c8b140d00e2b0147768296e9d275a2f7ef388e41c292f7eb5e658d5ebef")
    ]


def merkle_rewards_roots():
    return [
        HexBytes("0x0be72dfe7a5ee10d39d09e1fbdf2f75e8c7d4e9f2079be9973053ef4205760dc"),
        HexBytes("0x05e28855885eeda09c6805f28c133af15f2a75236649b608c45a1e996ae72780"),
        HexBytes("0xd1e41476c4047f9cab8855e0f44924486a10d16a679a58c9c06d51d606c59f42"),
        HexBytes("0x15845de2e97ce7f1083ad86c1a70fc567dc227b9ba5d69a8f642bcf4ea7edb19"),
        HexBytes("0x2bf1676c67774fa9204b598e8c3154b837573ddb6ac9a565acb9b797039b7aaa"),
        HexBytes("0xa85b1d21199afa07dc70c686d49c9362f6c6ea6ed02a9946efebe8d68bd344d4"),
        HexBytes("0xe00388ea813a2988a357b164a0e14601596793ade10c09d8b18df3dd0d6290d1"),
    ]


def merkle_vested_rewards_roots():
    return [
        HexBytes("0x98eae9d462d914ddc95e537dce14f1cfe204cfee6ed2e17342a729b6b020e87b"),
        HexBytes("0x783223891f4dc45c0bf9ed972c60852bf274332acfce6ee68ef522ce2d11ee7b"),
        HexBytes("0xb74d78fb97f55c7a66052490ced2a705f500306896ca7d277e0dd2510ea454cc"),
        HexBytes("0xf56209bae78f84e229e51ee74ee443d0ce3f2f703236f5c082d61d1cd79f2409"),
        HexBytes("0x144b8a7cd1a3515773567815008119bec4e2d271abf3444157be9f152a580c66"),
        HexBytes("0x202bec3a5eb253d27af62a97cec06e118464493569822dbd4847f13e2fed63fe"),
        HexBytes("0xbdd3da479389dd3a446a135c7f11e3a5e0d721a3436344beb6abcbf6b5095186"),
        HexBytes("0x578d08be95d68f91e191402bc6853125b4874c7e4d7b6260f0dc1c50fdb83279"),
        HexBytes("0xef0c82459daf220b86da257128e2300f825d910253ae8df419f8c6ef524f7227"),
        HexBytes("0x757fcec266eb09de3d813192a132e81e92d26beb92a15c0970a40595cccd9712"),
        HexBytes("0xa8584656c0a14dbf3fef625b8f4c506c14d386a4bd20dc8d6743216c288df194"),
        HexBytes("0x3382f6e5784b35fc7e5f2f7752ddd5102811d77d0dcb354e16e36b01d2b0606e"),
        HexBytes("0x0249d59efd59b551bb08403f8034cdffecef0a8ad600f2e5879d4c05a27cd9de"),
        HexBytes("0x77f2465eaaf77196ded6b7c943aaa9cb7a433e3e9701fe218d1decca58d3c2b9"),
        HexBytes("0x1eeab0179d98a0d4360c9545116a59a1c64dd6415fe1e8959bb99d29973eb830"),
        HexBytes("0xba0aacc0f0d46ca703906af99225962b861143bd71465a7480c0c23d1c953f32"),
        HexBytes("0x2c98ac483fb981452581bff4edc3f34a2015c5dba9ac7c6a02c284dcece428dd"),
        HexBytes("0x42b4e2736104c3547ca6d8b55f03cfb5d6b8389180b938718c3e489d4ecd0bb7"),
        HexBytes("0x66e1961787f72a7706c86cb12840914d72205151a8c75cce7d4f48f70b9a7412"),
        HexBytes("0x5ff319c4ef14bee4d144ccefe189feeae795bc7accf89e80fc349ffb338cd1bc"),
        HexBytes("0x61920a81e2e18adcc7952b7eba972d38b5ab4db36dcca8fd10dd259e371b7d2b"),
        HexBytes("0x07a017849273697263f365ccd252e636ee39621c59379e751c477c672f891409"),
        HexBytes("0x1b11b4994d9ac3e8683fb160fad85ac06643290ca6e6d94341ce5226f206c9da"),
        HexBytes("0x6917067a40942599463ebf1bbe3b11c1ff9f64653fc7a465ed8f69cb9b23a0a0"),
        HexBytes("0x11008dfcc447c90f8df6fb63650ed0acf6a3e7ef0251a924520edcaf91203cd6"),
        HexBytes("0x817d8b993d16c291c8fa365aad4413d904f606b75aadfc8ef527cc4dc4e50f30"),
        HexBytes("0x182f9e9bfc7c211a2d8d2ce62cc81a5251f8926a57a1d197fa0ef5f39bfc3d5f"),
        HexBytes("0xa1a42a56dfb1dae4c662a015aab63054d8dd69a5c44c8bae76875a61ab1dded1"),
        HexBytes("0x0cba2a92f0c52ad0255675f2641c876145bb2c0ea46d30ae62da4402c6df6c1b"),
        HexBytes("0xad356d6ac79480f0c1a192e095b545b7c5b378d940a81394c0ad422cbf8d8687"),
        HexBytes("0x283cdce093b0ea3639287e2e25f2406c6259df32a176627e577fbd49d402f326"),
        HexBytes("0x1049d497634b7ce289b4fdfc7d42006af6c3c68af584dbce45c11b78903edec6"),
        HexBytes("0xf35165acfc748c12e06dd3676161171fa300f9a2b7bc02dfd3e748692c985a91"),
        HexBytes("0xbe006aba4ca20d4d8471f73474555aa418baed272f98015b5c65fc40f3c350d1"),
    ]


pre_test_swap_adel_amount = 0
total_adel_swapped = 0
total_stake_withdrawn = 0
total_rewards_from_adel = 0
total_rewards_from_akro = 0
staking_adel_before = 0
rewards_on_adel_before = 0
rewards_on_akro_before = 0

total_adel_change = 0


def test_initial_balances(
    chain, owner, adel, vakro, vakroSwap, adelstakingpool, akrostakingpool
):
    global staking_adel_before
    staking_adel_before = adelstakingpool.totalStaked()
    global rewards_on_adel_before
    rewards_on_adel_before = (
        adel.balanceOf(adelstakingpool.address) - adelstakingpool.totalStaked()
    )
    global rewards_on_akro_before
    rewards_on_akro_before = adel.balanceOf(akrostakingpool.address)

    # Prepare vAkro and swap
    vakroSwap.setMerkleRoots(merkle_roots(), {"from": owner})
    start = chain.time() + 1000
    vakro.setVestingStart(start, {"from": owner})
    chain.mine(1)

    assert adel.balanceOf(vakro.address) == 0
    global pre_test_swap_adel_amount
    pre_test_swap_adel_amount = adel.balanceOf(vakroSwap.address)
    assert adel.balanceOf(adelstakingpool.address) != 0


def test_swap_adel_1(akro, adel, vakro, vakroSwap, adelstakingpool, akrostakingpool):
    proofs_dict = users_proofs()
    (
        user_for_wallet,
        user_for_stake,
        user_for_rewards,
        user_for_stake_reward,
        user_for_change,
        user_for_both_rewards,
    ) = get_users()

    ###
    #  Can swap from the wallet
    ###
    user_adel_balance_before = adel.balanceOf(user_for_wallet)
    swap_adel_balance_before = adel.balanceOf(vakroSwap.address)
    user_adel_staked_before = adelstakingpool.getPersonalStakeTotalAmount(
        user_for_wallet
    )
    user_adel_rewards_before = adelstakingpool.rewardBalanceOf(
        user_for_wallet, adel.address
    ) + akrostakingpool.rewardBalanceOf(user_for_wallet, adel.address)
    total_staked_before = adelstakingpool.totalStaked()

    assert vakroSwap.adelSwapped(user_for_wallet) == 0
    assert vakro.balanceOf(user_for_wallet) == 0

    adel.approve(
        vakroSwap.address,
        proofs_dict[user_for_wallet]["amount_wallet"],
        {"from": user_for_wallet},
    )
    vakroSwap.swapFromAdel(
        proofs_dict[user_for_wallet]["amount_wallet"],
        proofs_dict[user_for_wallet]["rootIndex"],
        proofs_dict[user_for_wallet]["maxAmount"],
        proofs_dict[user_for_wallet]["proofs"],
        {"from": user_for_wallet},
    )

    global total_adel_swapped
    total_adel_swapped += proofs_dict[user_for_wallet]["amount_wallet"]

    user_adel_balance_after = adel.balanceOf(user_for_wallet)
    swap_adel_balance_after = adel.balanceOf(vakroSwap.address)
    user_adel_staked_after = adelstakingpool.getPersonalStakeTotalAmount(
        user_for_wallet
    )
    user_adel_rewards_after = adelstakingpool.rewardBalanceOf(
        user_for_wallet, adel.address
    ) + akrostakingpool.rewardBalanceOf(user_for_wallet, adel.address)
    total_staked_after = adelstakingpool.totalStaked()

    assert (
        user_adel_balance_before - user_adel_balance_after
        == proofs_dict[user_for_wallet]["amount_wallet"]
    )
    assert (
        swap_adel_balance_after - swap_adel_balance_before
        == proofs_dict[user_for_wallet]["amount_wallet"]
    )

    assert total_staked_before == total_staked_after
    assert user_adel_staked_before == user_adel_staked_after
    assert user_adel_rewards_before == user_adel_rewards_after

    assert (
        vakro.balanceOf(user_for_wallet)
        == ADEL_AKRO_RATE * proofs_dict[user_for_wallet]["amount_wallet"]
    )
    assert (
        vakroSwap.adelSwapped(user_for_wallet)
        == proofs_dict[user_for_wallet]["amount_wallet"]
    )


def test_swap_adel_2(akro, adel, vakro, vakroSwap, adelstakingpool, akrostakingpool):
    proofs_dict = users_proofs()
    (
        user_for_wallet,
        user_for_stake,
        user_for_rewards,
        user_for_stake_reward,
        user_for_change,
        user_for_both_rewards,
    ) = get_users()

    ###
    # Can swap from the stake
    ###
    user_akro_balance_before = akro.balanceOf(user_for_stake)
    user_rewards_in_akro = adelstakingpool.rewardBalanceOf(user_for_stake, akro.address)
    user_adel_balance_before = adel.balanceOf(user_for_stake)
    swap_adel_balance_before = adel.balanceOf(vakroSwap.address)
    user_adel_staked_before = adelstakingpool.getPersonalStakeTotalAmount(
        user_for_stake
    )
    user_adel_rewards_before = adelstakingpool.rewardBalanceOf(
        user_for_stake, adel.address
    )
    total_staked_before = adelstakingpool.totalStaked()

    assert vakroSwap.adelSwapped(user_for_stake) == 0
    assert vakro.balanceOf(user_for_stake) == 0

    vakroSwap.swapFromStakedAdel(
        proofs_dict[user_for_stake]["rootIndex"],
        proofs_dict[user_for_stake]["maxAmount"],
        proofs_dict[user_for_stake]["proofs"],
        {"from": user_for_stake},
    )

    global total_adel_swapped
    total_adel_swapped += (
        proofs_dict[user_for_stake]["amount_stake"]
        + proofs_dict[user_for_stake]["amount_rewards_from_adel"]
    )
    global total_stake_withdrawn
    total_stake_withdrawn += proofs_dict[user_for_stake]["amount_stake"]
    global total_rewards_from_adel
    total_rewards_from_adel += proofs_dict[user_for_stake]["amount_rewards_from_adel"]

    user_akro_balance_after = akro.balanceOf(user_for_stake)
    user_adel_balance_after = adel.balanceOf(user_for_stake)
    swap_adel_balance_after = adel.balanceOf(vakroSwap.address)
    user_adel_staked_after = adelstakingpool.getPersonalStakeTotalAmount(user_for_stake)
    user_adel_rewards_after = adelstakingpool.rewardBalanceOf(
        user_for_stake, adel.address
    )
    total_staked_after = adelstakingpool.totalStaked()

    # AKRO has been sent to the user, protocols balance is unchanged
    assert user_akro_balance_after - user_akro_balance_before == user_rewards_in_akro
    assert adelstakingpool.rewardBalanceOf(user_for_stake, akro.address) == 0
    # Nothing left on the swap contract
    assert akro.balanceOf(vakroSwap.address) == 0

    assert user_adel_balance_before == user_adel_balance_after
    assert (
        swap_adel_balance_after - swap_adel_balance_before
        == proofs_dict[user_for_stake]["amount_stake"]
        + proofs_dict[user_for_stake]["amount_rewards_from_adel"]
    )

    assert (
        total_staked_before - total_staked_after
        == proofs_dict[user_for_stake]["amount_stake"]
    )
    assert user_adel_staked_after == 0
    assert user_adel_rewards_after == 0

    assert vakro.balanceOf(user_for_stake) == ADEL_AKRO_RATE * (
        proofs_dict[user_for_stake]["amount_stake"]
        + proofs_dict[user_for_stake]["amount_rewards_from_adel"]
    )
    assert (
        vakroSwap.adelSwapped(user_for_stake)
        == proofs_dict[user_for_stake]["amount_stake"]
        + proofs_dict[user_for_stake]["amount_rewards_from_adel"]
    )


def test_swap_adel_3(akro, adel, vakro, vakroSwap, adelstakingpool, akrostakingpool):
    proofs_dict = users_proofs()
    (
        user_for_wallet,
        user_for_stake,
        user_for_rewards,
        user_for_stake_reward,
        user_for_change,
        user_for_both_rewards,
    ) = get_users()

    ###
    # Can swap from rewards
    ###
    user_adel_balance_before = adel.balanceOf(user_for_rewards)
    swap_adel_balance_before = adel.balanceOf(vakroSwap.address)
    user_adel_staked_before = adelstakingpool.getPersonalStakeTotalAmount(
        user_for_rewards
    )
    user_adel_rewards_before = adelstakingpool.rewardBalanceOf(
        user_for_rewards, adel.address
    ) + akrostakingpool.rewardBalanceOf(user_for_rewards, adel.address)
    total_staked_before = adelstakingpool.totalStaked()

    assert vakroSwap.adelSwapped(user_for_rewards) == 0
    assert vakro.balanceOf(user_for_rewards) == 0

    vakroSwap.swapFromRewardAdel(
        proofs_dict[user_for_rewards]["rootIndex"],
        proofs_dict[user_for_rewards]["maxAmount"],
        proofs_dict[user_for_rewards]["proofs"],
        {"from": user_for_rewards},
    )

    global total_adel_swapped
    total_adel_swapped += proofs_dict[user_for_rewards]["amount_rewards"]
    global total_rewards_from_adel
    total_rewards_from_adel += proofs_dict[user_for_rewards]["amount_rewards"]

    user_adel_balance_after = adel.balanceOf(user_for_rewards)
    swap_adel_balance_after = adel.balanceOf(vakroSwap.address)
    user_adel_staked_after = adelstakingpool.getPersonalStakeTotalAmount(
        user_for_rewards
    )
    user_adel_rewards_after = adelstakingpool.rewardBalanceOf(
        user_for_rewards, adel.address
    ) + akrostakingpool.rewardBalanceOf(user_for_rewards, adel.address)
    total_staked_after = adelstakingpool.totalStaked()

    assert user_adel_balance_before == user_adel_balance_after
    assert (
        swap_adel_balance_after - swap_adel_balance_before
        == proofs_dict[user_for_rewards]["amount_rewards"]
    )

    assert total_staked_before == total_staked_after
    assert user_adel_staked_before == user_adel_staked_after
    assert user_adel_rewards_after == 0

    assert (
        vakro.balanceOf(user_for_rewards)
        == ADEL_AKRO_RATE * proofs_dict[user_for_rewards]["amount_rewards"]
    )
    assert (
        vakroSwap.adelSwapped(user_for_rewards)
        == proofs_dict[user_for_rewards]["amount_rewards"]
    )


def test_swap_adel_4(akro, adel, vakro, vakroSwap, adelstakingpool, akrostakingpool):
    proofs_dict = users_proofs()
    (
        user_for_wallet,
        user_for_stake,
        user_for_rewards,
        user_for_stake_reward,
        user_for_change,
        user_for_both_rewards,
    ) = get_users()

    ###
    # Can swap from stake and rewards
    ###
    user_adel_balance_before = adel.balanceOf(user_for_stake_reward)
    swap_adel_balance_before = adel.balanceOf(vakroSwap.address)
    user_adel_staked_before = adelstakingpool.getPersonalStakeTotalAmount(
        user_for_stake_reward
    )
    user_adel_rewards_before = adelstakingpool.rewardBalanceOf(
        user_for_stake_reward, adel.address
    ) + akrostakingpool.rewardBalanceOf(user_for_stake_reward, adel.address)
    total_staked_before = adelstakingpool.totalStaked()

    assert vakroSwap.adelSwapped(user_for_stake_reward) == 0
    assert vakro.balanceOf(user_for_stake_reward) == 0

    vakroSwap.swapFromRewardAdel(
        proofs_dict[user_for_stake_reward]["rootIndex"],
        proofs_dict[user_for_stake_reward]["maxAmount"],
        proofs_dict[user_for_stake_reward]["proofs"],
        {"from": user_for_stake_reward},
    )

    vakroSwap.swapFromStakedAdel(
        proofs_dict[user_for_stake_reward]["rootIndex"],
        proofs_dict[user_for_stake_reward]["maxAmount"],
        proofs_dict[user_for_stake_reward]["proofs"],
        {"from": user_for_stake_reward},
    )

    global total_adel_swapped
    total_adel_swapped += (
        proofs_dict[user_for_stake_reward]["amount_stake"]
        + proofs_dict[user_for_stake_reward]["amount_rewards"]
    )
    global total_stake_withdrawn
    total_stake_withdrawn += proofs_dict[user_for_stake_reward]["amount_stake"]
    global total_rewards_from_adel
    total_rewards_from_adel += proofs_dict[user_for_stake_reward]["amount_rewards"]

    user_adel_balance_after = adel.balanceOf(user_for_stake_reward)
    swap_adel_balance_after = adel.balanceOf(vakroSwap.address)
    user_adel_staked_after = adelstakingpool.getPersonalStakeTotalAmount(
        user_for_stake_reward
    )
    user_adel_rewards_after = adelstakingpool.rewardBalanceOf(
        user_for_stake_reward, adel.address
    ) + akrostakingpool.rewardBalanceOf(user_for_stake_reward, adel.address)
    total_staked_after = adelstakingpool.totalStaked()

    assert user_adel_balance_before == user_adel_balance_after
    assert (
        swap_adel_balance_after - swap_adel_balance_before
        == proofs_dict[user_for_stake_reward]["amount_stake"]
        + proofs_dict[user_for_stake_reward]["amount_rewards"]
    )

    assert (
        total_staked_before - total_staked_after
        == proofs_dict[user_for_stake_reward]["amount_stake"]
    )
    assert user_adel_staked_after == 0
    assert user_adel_rewards_after == 0

    assert vakro.balanceOf(user_for_stake_reward) == ADEL_AKRO_RATE * (
        proofs_dict[user_for_stake_reward]["amount_stake"]
        + proofs_dict[user_for_stake_reward]["amount_rewards"]
    )
    assert (
        vakroSwap.adelSwapped(user_for_stake_reward)
        == proofs_dict[user_for_stake_reward]["amount_stake"]
        + proofs_dict[user_for_stake_reward]["amount_rewards"]
    )


def test_swap_adel_5(akro, adel, vakro, vakroSwap, adelstakingpool, akrostakingpool):
    proofs_dict = users_proofs()
    (
        user_for_wallet,
        user_for_stake,
        user_for_rewards,
        user_for_stake_reward,
        user_for_change,
        user_for_both_rewards,
    ) = get_users()

    ###
    # Change is sent to the wallet
    ###
    user_adel_balance_before = adel.balanceOf(user_for_change)
    swap_adel_balance_before = adel.balanceOf(vakroSwap.address)
    user_adel_staked_before = adelstakingpool.getPersonalStakeTotalAmount(
        user_for_change
    )
    user_adel_rewards_before = adelstakingpool.rewardBalanceOf(
        user_for_change, adel.address
    ) + akrostakingpool.rewardBalanceOf(user_for_change, adel.address)
    total_staked_before = adelstakingpool.totalStaked()

    assert vakroSwap.adelSwapped(user_for_change) == 0
    assert vakro.balanceOf(user_for_change) == 0

    over_adel = proofs_dict[user_for_stake]["amount_wallet"]
    assert over_adel > 0 and over_adel < proofs_dict[user_for_change]["amount_stake"]
    adel.transfer(user_for_change, over_adel, {"from": user_for_stake})
    amount_to_swap = proofs_dict[user_for_change]["amount_wallet"] + over_adel
    adel.approve(vakroSwap.address, amount_to_swap, {"from": user_for_change})
    vakroSwap.swapFromAdel(
        amount_to_swap,
        proofs_dict[user_for_change]["rootIndex"],
        proofs_dict[user_for_change]["maxAmount"],
        proofs_dict[user_for_change]["proofs"],
        {"from": user_for_change},
    )

    vakroSwap.swapFromStakedAdel(
        proofs_dict[user_for_change]["rootIndex"],
        proofs_dict[user_for_change]["maxAmount"],
        proofs_dict[user_for_change]["proofs"],
        {"from": user_for_change},
    )

    global total_adel_swapped
    total_adel_swapped += amount_to_swap + proofs_dict[user_for_change]["amount_stake"]
    global total_stake_withdrawn
    total_stake_withdrawn += proofs_dict[user_for_change]["amount_stake"]

    user_adel_balance_after = adel.balanceOf(user_for_change)
    swap_adel_balance_after = adel.balanceOf(vakroSwap.address)
    user_adel_staked_after = adelstakingpool.getPersonalStakeTotalAmount(
        user_for_change
    )
    user_adel_rewards_after = adelstakingpool.rewardBalanceOf(
        user_for_change, adel.address
    ) + akrostakingpool.rewardBalanceOf(user_for_change, adel.address)
    total_staked_after = adelstakingpool.totalStaked()

    global total_adel_change
    total_adel_change = (
        amount_to_swap
        + proofs_dict[user_for_change]["amount_stake"]
        - proofs_dict[user_for_change]["maxAmount"]
    )

    assert (
        user_adel_balance_before - user_adel_balance_after
        == proofs_dict[user_for_change]["amount_wallet"] - total_adel_change
    )
    assert (
        swap_adel_balance_after - swap_adel_balance_before
        == proofs_dict[user_for_change]["maxAmount"]
    )

    assert (
        total_staked_before - total_staked_after
        == proofs_dict[user_for_change]["amount_stake"]
    )
    assert user_adel_staked_after == 0
    assert user_adel_rewards_after == 0

    assert (
        vakro.balanceOf(user_for_change)
        == ADEL_AKRO_RATE * proofs_dict[user_for_change]["maxAmount"]
    )
    assert (
        vakroSwap.adelSwapped(user_for_change)
        == proofs_dict[user_for_change]["maxAmount"]
    )


def test_swap_adel_6(akro, adel, vakro, vakroSwap, adelstakingpool, akrostakingpool):
    proofs_dict = users_proofs()
    (
        user_for_wallet,
        user_for_stake,
        user_for_rewards,
        user_for_stake_reward,
        user_for_change,
        user_for_both_rewards,
    ) = get_users()
    ###
    # Rewards from both stakings
    ###
    user_adel_balance_before = adel.balanceOf(user_for_both_rewards)
    swap_adel_balance_before = adel.balanceOf(vakroSwap.address)
    user_adel_staked_before = adelstakingpool.getPersonalStakeTotalAmount(
        user_for_both_rewards
    )
    user_adel_rewards_before = adelstakingpool.rewardBalanceOf(
        user_for_both_rewards, adel.address
    ) + akrostakingpool.rewardBalanceOf(user_for_both_rewards, adel.address)
    total_staked_before = adelstakingpool.totalStaked()

    assert vakroSwap.adelSwapped(user_for_both_rewards) == 0
    assert vakro.balanceOf(user_for_both_rewards) == 0

    vakroSwap.swapFromRewardAdel(
        proofs_dict[user_for_both_rewards]["rootIndex"],
        proofs_dict[user_for_both_rewards]["maxAmount"],
        proofs_dict[user_for_both_rewards]["proofs"],
        {"from": user_for_both_rewards},
    )

    global total_adel_swapped
    total_adel_swapped += proofs_dict[user_for_both_rewards]["amount_rewards"]
    global total_rewards_from_adel
    total_rewards_from_adel += proofs_dict[user_for_both_rewards][
        "amount_rewards_from_adel"
    ]
    global total_rewards_from_akro
    total_rewards_from_akro += proofs_dict[user_for_both_rewards][
        "amount_rewards_from_akro"
    ]

    user_adel_balance_after = adel.balanceOf(user_for_both_rewards)
    swap_adel_balance_after = adel.balanceOf(vakroSwap.address)
    user_adel_staked_after = adelstakingpool.getPersonalStakeTotalAmount(
        user_for_both_rewards
    )
    user_adel_rewards_after = adelstakingpool.rewardBalanceOf(
        user_for_both_rewards, adel.address
    ) + akrostakingpool.rewardBalanceOf(user_for_both_rewards, adel.address)
    total_staked_after = adelstakingpool.totalStaked()

    assert user_adel_balance_before == user_adel_balance_after
    assert (
        swap_adel_balance_after - swap_adel_balance_before
        == proofs_dict[user_for_both_rewards]["amount_rewards"]
    )

    assert total_staked_before == total_staked_after
    assert user_adel_staked_after == user_adel_staked_before
    assert user_adel_rewards_after == 0

    assert (
        vakro.balanceOf(user_for_both_rewards)
        == ADEL_AKRO_RATE * proofs_dict[user_for_both_rewards]["amount_rewards"]
    )
    assert (
        vakroSwap.adelSwapped(user_for_both_rewards)
        == proofs_dict[user_for_both_rewards]["amount_rewards"]
    )


def test_final_balances(adel, akro, vakro, vakroSwap, adelstakingpool, akrostakingpool):
    ###
    # All calculations match
    ###
    staking_adel_after = adelstakingpool.totalStaked()
    rewards_on_adel_after = (
        adel.balanceOf(adelstakingpool.address) - adelstakingpool.totalStaked()
    )
    rewards_on_akro_after = adel.balanceOf(akrostakingpool.address)

    global total_adel_swapped
    global total_adel_change
    global total_stake_withdrawn
    global total_rewards_from_adel
    global total_rewards_from_akro
    global staking_adel_before
    global rewards_on_adel_before
    global rewards_on_akro_before

    assert (
        adel.balanceOf(vakroSwap.address)
        == pre_test_swap_adel_amount + total_adel_swapped - total_adel_change
    )
    assert staking_adel_before - staking_adel_after == total_stake_withdrawn
    assert rewards_on_adel_before - rewards_on_adel_after == total_rewards_from_adel
    assert rewards_on_akro_before - rewards_on_akro_after == total_rewards_from_akro
    assert akro.balanceOf(vakroSwap.address) == 0
    assert vakro.balanceOf(vakroSwap.address) == 0


def test_post_update(owner, vakroSwap):
    proofs_dict = users_proofs()
    (
        user_for_wallet,
        user_for_stake,
        user_for_rewards,
        user_for_stake_reward,
        user_for_change,
        user_for_both_rewards,
    ) = get_users()

    assert (
        vakroSwap.adelSwapped(user_for_wallet)
        == proofs_dict[user_for_wallet]["amount_wallet"]
    )
    assert (
        vakroSwap.adelSwapped(user_for_stake)
        == proofs_dict[user_for_stake]["amount_stake"]
        + proofs_dict[user_for_stake]["amount_rewards_from_adel"]
    )
    assert (
        vakroSwap.adelSwapped(user_for_rewards)
        == proofs_dict[user_for_rewards]["amount_rewards"]
    )
    assert (
        vakroSwap.adelSwapped(user_for_stake_reward)
        == proofs_dict[user_for_stake_reward]["amount_stake"]
        + proofs_dict[user_for_stake_reward]["amount_rewards"]
    )
    assert (
        vakroSwap.adelSwapped(user_for_change)
        == proofs_dict[user_for_change]["maxAmount"]
    )
    assert (
        vakroSwap.adelSwapped(user_for_both_rewards)
        == proofs_dict[user_for_both_rewards]["amount_rewards"]
    )


def test_rewards(owner, adel, akro, vakro, vakroVestingSwap, vakroSwap):
    vakroSwap.withdrawAdel(owner, {"from": owner})
    vakro.addMinter(vakroVestingSwap.address, {"from": owner})
    vakro.addSender(vakroVestingSwap.address, {"from": owner})
    vakroVestingSwap.setMerkleWalletRewardsRoots(
        merkle_rewards_roots(), {"from": owner}
    )
    vakroVestingSwap.setMerkleVestedRewardsRoots(
        merkle_vested_rewards_roots(), {"from": owner}
    )
    vakroVestingSwap.setSwapRate(15, 1, {"from": owner})

    proofs_dict = users_rewards_proofs()
    user_for_wallet, user_for_vesting = get_rewards_users()
    adel.transfer(
        user_for_wallet,
        2 * proofs_dict[user_for_wallet]["amount_wallet"],
        {"from": owner},
    )

    ###
    # Test with rewards from the wallet
    ###
    user_adel_balance_before = adel.balanceOf(user_for_wallet)
    swap_adel_balance_before = adel.balanceOf(vakroVestingSwap.address)
    adel_total_swapped_before = vakroSwap.adelSwapped(user_for_wallet)
    adel_rewards_total_swapped_before = vakroVestingSwap.adelRewardsSwapped(
        user_for_wallet
    )
    vakro_balance_before = vakro.balanceOf(user_for_wallet)

    assert adel_rewards_total_swapped_before == 0
    assert vakro.balanceOf(user_for_wallet) == 0

    adel.approve(
        vakroVestingSwap.address,
        proofs_dict[user_for_wallet]["amount_wallet"],
        {"from": user_for_wallet},
    )
    vakroVestingSwap.swapFromAdelWalletRewards(
        proofs_dict[user_for_wallet]["amount_wallet"],
        proofs_dict[user_for_wallet]["rootIndex"],
        proofs_dict[user_for_wallet]["maxAmount"],
        proofs_dict[user_for_wallet]["proofs"],
        {"from": user_for_wallet},
    )

    global total_adel_swapped
    total_adel_swapped += proofs_dict[user_for_wallet]["amount_wallet"]

    user_adel_balance_after = adel.balanceOf(user_for_wallet)
    swap_adel_balance_after = adel.balanceOf(vakroVestingSwap.address)
    adel_total_swapped_after = vakroSwap.adelSwapped(user_for_wallet)
    adel_rewards_total_swapped_after = vakroVestingSwap.adelRewardsSwapped(
        user_for_wallet
    )
    vakro_balance_after = vakro.balanceOf(user_for_wallet)

    assert (
        user_adel_balance_before - user_adel_balance_after
        == proofs_dict[user_for_wallet]["amount_wallet"]
    )
    assert (
        swap_adel_balance_after - swap_adel_balance_before
        == proofs_dict[user_for_wallet]["amount_wallet"]
    )

    assert adel_total_swapped_before == adel_total_swapped_after
    assert (
        adel_rewards_total_swapped_after - adel_rewards_total_swapped_before
        == proofs_dict[user_for_wallet]["amount_wallet"]
    )

    assert (
        vakro_balance_after - vakro_balance_before
        == ADEL_AKRO_RATE * proofs_dict[user_for_wallet]["amount_wallet"]
    )

    ###
    # Test with vesting revards
    ###
    user_adel_balance_before = adel.balanceOf(user_for_vesting)
    swap_adel_balance_before = adel.balanceOf(vakroVestingSwap.address)
    adel_total_swapped_before = vakroSwap.adelSwapped(user_for_vesting)
    adel_rewards_total_swapped_before = vakroVestingSwap.adelRewardsSwapped(
        user_for_vesting
    )
    vakro_balance_before = vakro.balanceOf(user_for_vesting)

    assert adel_rewards_total_swapped_before == 0
    assert vakro.balanceOf(user_for_vesting) == 0

    vakroVestingSwap.swapFromAdelVestedRewards(
        proofs_dict[user_for_vesting]["rootIndex"],
        proofs_dict[user_for_vesting]["maxAmount"],
        proofs_dict[user_for_vesting]["proofs"],
        proofs_dict[user_for_vesting]["rootIndexVested"],
        proofs_dict[user_for_vesting]["maxAmountVested"],
        proofs_dict[user_for_vesting]["proofsVested"],
        {"from": user_for_vesting},
    )

    vested_amount_swapped = (
        proofs_dict[user_for_vesting]["maxAmountVested"]
        - proofs_dict[user_for_vesting]["maxAmount"]
    )
    total_adel_swapped += vested_amount_swapped

    user_adel_balance_after = adel.balanceOf(user_for_vesting)
    swap_adel_balance_after = adel.balanceOf(vakroVestingSwap.address)
    adel_total_swapped_after = vakroSwap.adelSwapped(user_for_vesting)
    adel_rewards_total_swapped_after = vakroVestingSwap.adelRewardsSwapped(
        user_for_vesting
    )
    vakro_balance_after = vakro.balanceOf(user_for_vesting)

    assert user_adel_balance_before == user_adel_balance_after
    assert swap_adel_balance_after == swap_adel_balance_before

    assert adel_total_swapped_before == adel_total_swapped_after
    assert (
        adel_rewards_total_swapped_after - adel_rewards_total_swapped_before
        == vested_amount_swapped
    )

    assert (
        vakro_balance_after - vakro_balance_before
        == ADEL_AKRO_RATE * vested_amount_swapped
    )
