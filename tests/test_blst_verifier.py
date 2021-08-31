from lido.blstverify import verify


def test_valid_bls():
    pubkey = bytearray(
        b"\xad\xd9\xa5\x0b\xc6\xde5B\xc8\x81\xe3e\x07\x99JRh5&\xf7]\xdc\xef,U\xe5\x05t\xc5\xc6^\xbd\x97?\xffHGWb\x9d\xed\x05\xe4~\xf2\xbf\xd56"
    )
    signing_root = bytearray(
        b"\x84\xd6\xcd{l\xb0\xfb\x00\x94\x95A\x07}-in,\x8f\xf0.\xc1i\x98\xd5!\x9d\xed^\xd2\x84\xf9l"
    )
    signature = bytearray(
        b"\x85\xe6\x14_\xee\x91np\xbb\xa6\x95\x15F1\x03\x1b\x97r\xedS\xe5Y\x0b<2XP7g)\x88\xcbg-\t\xab\xcd\x17\x12\x9e\x87\x0f\x15SdK\xa2^\x10)\xf5\xf9\xd2\xeb\x11\xc0\xe8c\xb3P\xb4\x1dm1\x8b\x9eC\xb7\xa2\xdb\xec\xf2\xdb[\xb3\x12\xf4\x0c\xab\x99\x0bG\x1f5\xfb\x10\x15w\xc4\xaby#\xca{\x03l"
    )

    res = verify(pubkey, signing_root, signature)

    assert res is True
    print(res)


def test_invalid_pubkey():
    pubkey = bytearray(
        b"\xaa\xd9\xa5\x0b\xc6\xde5B\xc8\x81\xe3e\x07\x99JRh5&\xf7]\xdc\xef,U\xe5\x05t\xc5\xc6^\xbd\x97?\xffHGWb\x9d\xed\x05\xe4~\xf2\xbf\xd56"
    )
    signing_root = bytearray(
        b"\x84\xd6\xcd{l\xb0\xfb\x00\x94\x95A\x07}-in,\x8f\xf0.\xc1i\x98\xd5!\x9d\xed^\xd2\x84\xf9l"
    )
    signature = bytearray(
        b"\x85\xe6\x14_\xee\x91np\xbb\xa6\x95\x15F1\x03\x1b\x97r\xedS\xe5Y\x0b<2XP7g)\x88\xcbg-\t\xab\xcd\x17\x12\x9e\x87\x0f\x15SdK\xa2^\x10)\xf5\xf9\xd2\xeb\x11\xc0\xe8c\xb3P\xb4\x1dm1\x8b\x9eC\xb7\xa2\xdb\xec\xf2\xdb[\xb3\x12\xf4\x0c\xab\x99\x0bG\x1f5\xfb\x10\x15w\xc4\xaby#\xca{\x03l"
    )

    res = verify(pubkey, signing_root, signature)

    assert res is False
    print(res)


def test_invalid_signing_root():
    pubkey = bytearray(
        b"\xad\xd9\xa5\x0b\xc6\xde5B\xc8\x81\xe3e\x07\x99JRh5&\xf7]\xdc\xef,U\xe5\x05t\xc5\xc6^\xbd\x97?\xffHGWb\x9d\xed\x05\xe4~\xf2\xbf\xd56"
    )
    signing_root = bytearray(
        b"\x83\xd6\xcd{l\xb0\xfb\x00\x94\x95A\x07}-in,\x8f\xf0.\xc1i\x98\xd5!\x9d\xed^\xd2\x84\xf9l"
    )
    signature = bytearray(
        b"\x85\xe6\x14_\xee\x91np\xbb\xa6\x95\x15F1\x03\x1b\x97r\xedS\xe5Y\x0b<2XP7g)\x88\xcbg-\t\xab\xcd\x17\x12\x9e\x87\x0f\x15SdK\xa2^\x10)\xf5\xf9\xd2\xeb\x11\xc0\xe8c\xb3P\xb4\x1dm1\x8b\x9eC\xb7\xa2\xdb\xec\xf2\xdb[\xb3\x12\xf4\x0c\xab\x99\x0bG\x1f5\xfb\x10\x15w\xc4\xaby#\xca{\x03l"
    )

    res = verify(pubkey, signing_root, signature)

    assert res is False
    print(res)


def test_invalid_signature():
    pubkey = bytearray(
        b"\xad\xd9\xa5\x0b\xc6\xde5B\xc8\x81\xe3e\x07\x99JRh5&\xf7]\xdc\xef,U\xe5\x05t\xc5\xc6^\xbd\x97?\xffHGWb\x9d\xed\x05\xe4~\xf2\xbf\xd56"
    )
    signing_root = bytearray(
        b"\x84\xd6\xcd{l\xb0\xfb\x00\x94\x95A\x07}-in,\x8f\xf0.\xc1i\x98\xd5!\x9d\xed^\xd2\x84\xf9l"
    )
    signature = bytearray(
        b"\x85\xe5\x14_\xee\x91np\xbb\xa6\x95\x15F1\x03\x1b\x97r\xedS\xe5Y\x0b<2XP7g)\x88\xcbg-\t\xab\xcd\x17\x12\x9e\x87\x0f\x15SdK\xa2^\x10)\xf5\xf9\xd2\xeb\x11\xc0\xe8c\xb3P\xb4\x1dm1\x8b\x9eC\xb7\xa2\xdb\xec\xf2\xdb[\xb3\x12\xf4\x0c\xab\x99\x0bG\x1f5\xfb\x10\x15w\xc4\xaby#\xca{\x03l"
    )

    res = verify(pubkey, signing_root, signature)

    assert res is False
    print(res)
