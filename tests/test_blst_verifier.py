from lido_sdk.blstverify import verify
from tests.fixtures import (
    VALID_KEY_BYTEARRAY,
    VALID_KEY_BYTES,
    INVALID_KEY_BYTEARRAY,
    INVALID_KEY_BYTES,
)


def test_valid_bls_bytearray():
    pubkey = VALID_KEY_BYTEARRAY["pubkey"]
    signing_root = VALID_KEY_BYTEARRAY["signing_root"]
    signature = VALID_KEY_BYTEARRAY["signature"]

    res = verify(pubkey, signing_root, signature)

    assert res is True


def test_invalid_bls_bytearray():
    pubkey = INVALID_KEY_BYTEARRAY["pubkey"]
    signing_root = INVALID_KEY_BYTEARRAY["signing_root"]
    signature = INVALID_KEY_BYTEARRAY["signature"]

    res = verify(pubkey, signing_root, signature)

    assert res is False


def test_valid_bls_bytes():
    pubkey = VALID_KEY_BYTES["pubkey"]
    signing_root = VALID_KEY_BYTES["signing_root"]
    signature = VALID_KEY_BYTES["signature"]

    res = verify(pubkey, signing_root, signature)

    assert res is True


def test_invalid_bls_bytes():
    pubkey = INVALID_KEY_BYTES["pubkey"]
    signing_root = INVALID_KEY_BYTES["signing_root"]
    signature = INVALID_KEY_BYTES["signature"]

    res = verify(pubkey, signing_root, signature)

    assert res is False


def test_empty_pubkey():
    pubkey = bytearray()
    signing_root = VALID_KEY_BYTEARRAY["signing_root"]
    signature = VALID_KEY_BYTEARRAY["signature"]

    res = verify(pubkey, signing_root, signature)

    assert res is False


def test_invalid_pubkey():
    pubkey = INVALID_KEY_BYTEARRAY["pubkey"]
    signing_root = VALID_KEY_BYTEARRAY["signing_root"]
    signature = VALID_KEY_BYTEARRAY["signature"]

    res = verify(pubkey, signing_root, signature)

    assert res is False


def test_invalid_signing_root():
    pubkey = VALID_KEY_BYTEARRAY["pubkey"]
    signing_root = INVALID_KEY_BYTEARRAY["signing_root"]
    signature = VALID_KEY_BYTEARRAY["signature"]

    res = verify(pubkey, signing_root, signature)

    assert res is False


def test_empty_signing_root():
    pubkey = VALID_KEY_BYTEARRAY["pubkey"]
    signing_root = bytearray()
    signature = VALID_KEY_BYTEARRAY["signature"]

    res = verify(pubkey, signing_root, signature)

    assert res is False


def test_invalid_signature():
    pubkey = VALID_KEY_BYTEARRAY["pubkey"]
    signing_root = INVALID_KEY_BYTEARRAY["signing_root"]
    signature = INVALID_KEY_BYTEARRAY["signature"]

    res = verify(pubkey, signing_root, signature)

    assert res is False


def test_empty_signature():
    pubkey = VALID_KEY_BYTEARRAY["pubkey"]
    signing_root = VALID_KEY_BYTEARRAY["signing_root"]
    signature = bytearray()

    res = verify(pubkey, signing_root, signature)

    assert res is False


def test_invalid_string_arguments():
    pubkey = ""
    signing_root = ""
    signature = ""

    res = verify(pubkey, signing_root, signature)

    assert res is False


def test_invalid_int_arguments():
    pubkey = 10
    signing_root = 20
    signature = 30

    res = verify(pubkey, signing_root, signature)

    assert res is False


def test_invalid_bool_arguments():
    pubkey = True
    signing_root = False
    signature = True

    res = verify(pubkey, signing_root, signature)

    assert res is False


def test_invalid_bytes_arguments():
    pubkey = bytes()
    signing_root = bytes()
    signature = bytes()

    res = verify(pubkey, signing_root, signature)

    assert res is False
