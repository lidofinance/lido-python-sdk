from typing import Tuple, Any
from eth2deposit.utils.ssz import DepositMessage, compute_signing_root
from .blst import PT, Pairing, P1_Affine, P2_Affine, BLST_SUCCESS

HASH_OR_ENCODE = True
DST = "BLS_SIG_BLS12381G2_XMD:SHA-256_SSWU_RO_POP_"
REQUIRED_DEPOSIT_ETH = 32
ETH2GWEI = 10 ** 9
AMOUNT = REQUIRED_DEPOSIT_ETH * ETH2GWEI


def get_signing_root(pubkey: bytes, wc: bytes, domain: bytes):
    deposit_message = DepositMessage(
        pubkey=pubkey,
        withdrawal_credentials=wc,
        amount=AMOUNT,
    )

    return compute_signing_root(deposit_message, domain)


def verify(pubkey: bytes, message: bytes, signature: bytes) -> bool:
    pk_affine = P1_Affine(pubkey)
    sig_affine = P2_Affine(signature)

    ctx = Pairing(HASH_OR_ENCODE, DST)
    result = ctx.aggregate(pk_affine, sig_affine, message)
    if result != BLST_SUCCESS:
        raise Exception(result)

    ctx.commit()
    gtsig = PT(sig_affine)

    return ctx.finalverify(gtsig)


def validate_key_blst(pubkey: bytes, signature: bytes, domain: bytes, wc: bytes) -> Tuple[bool, Any]:
    for (wc_hash, wc_desc) in wc.items():
        wc_bytes = bytes.fromhex(wc_hash[2:])
        signing_root = get_signing_root(pubkey, wc_bytes, domain)
        result = verify(pubkey, signing_root, signature)

        if result is True:
            return True, wc_desc

    return False, None
