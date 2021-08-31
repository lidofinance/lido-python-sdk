#!/usr/bin/env python3

import os
import sys
import re
import hashlib

print("testing...") or sys.stdout.flush()
########################################################################
import blst

msg = b"assertion"  # this what we're signing
DST = b"MY-DST"  # domain separation tag

SK = blst.SecretKey()
SK.keygen(b"*" * 32)  # secret key

########################################################################
# generate public key and signature

pk_for_wire = blst.P1(SK).serialize()

#                               # optional vvvvvvvvvvv augmentation
sig_for_wire = blst.P2().hash_to(msg, DST, pk_for_wire).sign_with(SK).serialize()

########################################################################
# at this point 'pk_for_wire', 'sig_for_wire' and 'msg' are
# "sent over network," so now on "receiver" side

sig = blst.P2_Affine(sig_for_wire)
pk = blst.P1_Affine(pk_for_wire)
if not pk.in_group():  # vet the public key
    raise AssertionError("disaster")
ctx = blst.Pairing(True, DST)
ctx.aggregate(pk, sig, msg, pk_for_wire)
ctx.commit()
if not ctx.finalverify():
    raise AssertionError("disaster")

########################################################################
# generate public key and signature

pk_for_wire = blst.P2(SK).serialize()

#                               # optional vvvvvvvvvvv augmentation
sig_for_wire = blst.P1().hash_to(msg, DST, pk_for_wire).sign_with(SK).serialize()

########################################################################
# at this point 'pk_for_wire', 'sig_for_wire' and 'msg' are
# "sent over network," so now on "receiver" side

sig = blst.P1_Affine(sig_for_wire)
pk = blst.P2_Affine(pk_for_wire)
if not pk.in_group():  # vet the public key
    raise AssertionError("disaster")
ctx = blst.Pairing(True, DST)
ctx.aggregate(pk, sig, msg, pk_for_wire)
ctx.commit()
if not ctx.finalverify():
    raise AssertionError("disaster")

if sys.version_info.major < 3:
    print("OK")
    sys.exit(0)

########################################################################
# from https://github.com/supranational/blst/issues/5

pk_for_wire = bytes.fromhex(
    "ab10fc693d038b73d67279127501a05f0072cbb7147c68650ef6ac4e0a413e5cabd1f35c8711e1f7d9d885bbc3b8eddc"
)
sig_for_wire = bytes.fromhex(
    "a44158c08c8c584477770feec2afa24d5a0b0bab2800414cb9efbb37c40339b6318c9349dad8de27ae644376d71232580ff5102c7a8579a6d2627c6e40b0ced737a60c66c7ebd377c04bf5ac957bf05bc8b6b09fbd7bdd2a7fa1090b5a0760bb"
)
msg = bytes.fromhex("0000000000000000000000000000000000000000000000000000000000000000")
DST = bytes.fromhex(
    "424c535f5349475f424c53313233383147325f584d443a5348412d3235365f535357555f524f5f504f505f"
)

sig = blst.P2_Affine(sig_for_wire)
pk = blst.P1_Affine(pk_for_wire)
if not pk.in_group():  # vet the public key
    raise AssertionError("disaster")
if sig.core_verify(pk, True, msg, DST) != blst.BLST_SUCCESS:
    raise AssertionError("disaster")

########################################################################
# test vectors from draft-irtf-cfrg-hash-to-curve

try:
    import json
    import glob

    coord = re.compile(r"0x([0-9a-f]+)(?:\s*,\s*0x([0-9a-f]+))?", re.IGNORECASE)

    def serialize_json_point(P):
        ret = b""
        x = coord.search(P["x"])
        if x.group(2):
            ret += bytes.fromhex(x.group(2))
        ret += bytes.fromhex(x.group(1))
        y = coord.search(P["y"])
        if y.group(2):
            ret += bytes.fromhex(y.group(2))
        ret += bytes.fromhex(y.group(1))
        return ret

    root_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../")
    vector_files_path = os.path.join(
        root_dir, "blst/bindings/vectors/hash_to_curve/*.json"
    )
    print("Looking into vector files at", vector_files_path)

    vector_files = glob.glob(vector_files_path)
    assert len(vector_files) == 4
    for file in vector_files:
        print(file)
        data = json.load(open(file))

        if data["curve"] == "BLS12-381 G1":
            point = blst.P1()
        else:
            point = blst.P2()

        DST = bytes(data["dst"], "ascii")

        if data["randomOracle"]:
            func = "point.hash_to(msg, DST).serialize()"
        else:
            func = "point.encode_to(msg, DST).serialize()"

        for vec in data["vectors"]:
            msg = bytes(vec["msg"], "ascii")
            if eval(func) != serialize_json_point(vec["P"]):
                raise AssertionError(msg)
except ModuleNotFoundError:
    print("skipping hash-to-curve KATs")

########################################################################
# test multi-scalar multiplication for self-consistency

points = []
scalars = []
total = 0
for _ in range(0, 42):
    p = os.urandom(8)
    s = int.from_bytes(os.urandom(8), "big")
    points.append(blst.G1().mult(p))
    scalars.append(s)
    total += s * int.from_bytes(p, "little")
a = blst.P1s.mult_pippenger(blst.P1s.to_affine(points), scalars)
if not a.is_equal(blst.G1().mult(total)):
    raise AssertionError("disaster")

points = []
scalars = []
total = 0
for _ in range(0, 42):
    p = os.urandom(8)
    s = int.from_bytes(os.urandom(8), "big")
    points.append(blst.G2().mult(p))
    scalars.append(s)
    total += s * int.from_bytes(p, "little")
a = blst.P2s.mult_pippenger(blst.P2s.to_affine(points), scalars)
if not a.is_equal(blst.G2().mult(total)):
    raise AssertionError("disaster")

########################################################################
# rudimentary blind signature PoC

# Signer's public key, implicitly trusted.
PK = blst.P1(SK).to_affine()

# User wants to have |msg| signed,
H_msg = blst.P2().hash_to(msg, DST)
# chooses random |r|,
r = blst.Scalar().from_bendian(os.urandom(32))  # should be PRF in real life...
# blinds the H(|msg|) with |r| and sends it to the Signer.
msg_for_wire = H_msg.dup().sign_with(r).serialize()

# Signer signs and sends the result back to the User.
blind_msg = blst.P2(msg_for_wire)
if not blind_msg.in_group():  # is User messing with Signer?
    raise AssertionError("disaster")
sig_for_wire = blind_msg.sign_with(SK).serialize()

# User ...
signature = blst.P2(sig_for_wire)
if not signature.in_group():  # is Signer messing with User?
    raise AssertionError("disaster")
# unblinds the result with 1/|r| to produce the actual |signature|,
signature = signature.sign_with(r.inverse()).to_affine()
# and double-checks if the Signer was honest?
C1 = blst.PT(signature)
C2 = blst.PT(H_msg.to_affine(), PK)
if not blst.PT.finalverify(C1, C2):
    raise AssertionError("disaster")

# Now |signature| can be verified as any other, e.g....
ctx = blst.Pairing(True, DST)
ctx.aggregate(PK, signature, msg)
ctx.commit()
if not ctx.finalverify():
    raise AssertionError("disaster")

########################################################################
# [a variant of] BBS+ PoC, https://eprint.iacr.org/2008/136.pdf

# Signer's public key, implicitly trusted.
w = blst.P2(SK)
w_for_wire = w.compress()

### The block of messages

msgs = ["assertion1", "assertion2", "assertion3", "assertionN"]
m = []
for msg in msgs:
    h = hashlib.sha512()
    h.update(msg.encode("utf-8"))
    m.append(blst.Scalar().from_bendian(h.digest()))

### Everybody involved:

count = len(msgs)
g = []
for i in range(count + 1):
    g.append(
        blst.P1().hash_to(
            b"\0" + i.to_bytes(4, "big") + b"\0" + count.to_bytes(4, "big"),
            DST,
            w_for_wire,
        )
    )

### Signing the block of messages.

e = blst.Scalar().from_bendian(os.urandom(32))  # should be PRF in real life...
s = blst.Scalar().from_bendian(os.urandom(32))

a = blst.G1().add(g[0].dup().mult(s))
for i in range(count):
    a.add(g[i + 1].dup().mult(m[i]))

A = a.dup().sign_with(e.dup().add(SK).inverse()).to_affine()

signature = [A, e, s]  # serialize to application liking

### Signature Verification.
# Verifier deserializes |signature|, recalculates |a| and verifies.
A, e, s = signature  # fake deserialization
a = blst.G1().add(g[0].dup().mult(s))
for i in range(count):
    a.add(g[i + 1].dup().mult(m[i]))

if not A.in_group():
    AssertionError("disaster")
C1 = blst.PT(blst.G2().mult(e).add(w).to_affine(), A)
C2 = blst.PT(a.to_affine())
if not blst.PT.finalverify(C1, C2):
    raise AssertionError("disaster")

### Blind-signing Committed Block of Messages.

# User creates |commitment| and sends it to Signer.
s_prime = blst.Scalar().from_bendian(os.urandom(32))
commitment = g[0].dup().sign_with(s_prime)
for i in range(count):
    commitment.add(g[i + 1].dup().mult(m[i]))

# Signer challenges User with |c|.
c = blst.Scalar().from_bendian(os.urandom(32))
# User provides proof of commitment.
s_tilde = blst.Scalar().from_bendian(os.urandom(32))
ZK = g[0].dup().sign_with(s_tilde)
r = [s_tilde.add(c.dup().mul(s_prime))]
for i in range(count):
    r.append(blst.Scalar().from_bendian(os.urandom(32)))
    ZK.add(g[i + 1].dup().mult(r[-1]))
    r[-1].add(c.dup().mul(m[i]))
# Signer verifies the proof, |ZK| and |r|.
ZK_verify = commitment.dup().neg().mult(c)
for i in range(count + 1):
    ZK_verify.add(g[i].dup().mult(r[i]))
if not ZK_verify.is_equal(ZK):
    raise AssertionError("disaster")

# Signer signs the |commitment| and sends the |blind_signature| back.
if not commitment.in_group():  # is User messing with Signer?
    raise AssertionError("disaster")
e = blst.Scalar().from_bendian(os.urandom(32))
s_pprime = blst.Scalar().from_bendian(os.urandom(32))

A = (
    blst.G1()
    .add(g[0].dup().mult(s_pprime))
    .add(commitment)
    .sign_with(e.dup().add(SK).inverse())
    .to_affine()
)

blind_signature = [A, e, s_pprime]  # serialize to application liking

# User unblinds the |blind_signature| by adding |s_prime| and |s_pprime|.
signature = blind_signature.copy()  # fake deserialization
if not signature[0].in_group():  # is Signer messing with User?
    raise AssertionError("disaster")
signature[2].add(s_prime)  # serialize to application liking

### Signature Verification.
# Verifier deserializes |signature|, recalculates |a| and verifies.
A, e, s = signature  # fake deserialization
a = blst.G1().add(g[0].dup().mult(s))
for i in range(count):
    a.add(g[i + 1].dup().mult(m[i]))

if not A.in_group():
    raise AssertionError("disaster")
C1 = blst.PT(blst.G2().mult(e).add(w).to_affine(), A)
C2 = blst.PT(a.to_affine())
if not blst.PT.finalverify(C1, C2):
    raise AssertionError("disaster")

########################################################################
# low-order points

p11 = blst.P1(
    bytes.fromhex(
        "80803f0d09fec09a95f2ee7495323c15c162270c7cceaffa8566e941c66bcf206e72955d58b3b32e564de3209d672ca5"
    )
)
if p11.in_group():
    raise AssertionError("disaster")
if not p11.mult(11).is_inf():
    raise AssertionError("disaster")

p13 = blst.P2(
    bytes.fromhex(
        "808514e6f6c41ddb685cd8e351d7cb2ee891d54d5850d42c440365b15dd8ab06b53da9ebb22bc31cea2234d30499b09f01b290cae398ecc1fda3d4beb248af58bd351c3d99a5b6c770fdb54bf46b123261b55cf0762aeef2341e35e90608fc31"
    )
)
if p13.in_group():
    raise AssertionError("disaster")
if not p13.mult(13).is_inf():
    raise AssertionError("disaster")

p23 = blst.P2(
    bytes.fromhex(
        "acaaaa268d201642af7eeb2c46b03ecf8af71b902f652884577e52994047fcde2f8b5d931fdacb2575937b72ef2d3b0c0da315f7c31904614d8110d493d1d7a00da97d5b640be19e4cc5dd302ad8e17aa853035d7a56e5c24347164c186d6d00"
    )
)
if p23.in_group():
    raise AssertionError("disaster")
if not p23.mult(23).is_inf():
    raise AssertionError("disaster")

print("OK")
