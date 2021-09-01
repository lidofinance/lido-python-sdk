from .blst import PT, Pairing, P1_Affine, P2_Affine, BLST_SUCCESS

HASH_OR_ENCODE = True
DST = "BLS_SIG_BLS12381G2_XMD:SHA-256_SSWU_RO_POP_"
VALID_TYPES = (bytes, bytearray)


def verify(pubkey: bytes, message: bytes, signature: bytes) -> bool:
    if (
        (not isinstance(pubkey, VALID_TYPES))
        or (not isinstance(message, VALID_TYPES))
        or (not isinstance(signature, VALID_TYPES))
    ):
        return False

    try:
        pk_affine = P1_Affine(pubkey)
        sig_affine = P2_Affine(signature)

        ctx = Pairing(HASH_OR_ENCODE, DST)
        result = ctx.aggregate(pk_affine, sig_affine, message)
        if result != BLST_SUCCESS:
            return False

        ctx.commit()
        gtsig = PT(sig_affine)

        return ctx.finalverify(gtsig)
    except RuntimeError:
        return False
