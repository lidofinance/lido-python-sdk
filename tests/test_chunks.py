from pytest import raises
from typing import List
from lido.chunks import get_chunks, Chunk


"""Test arguments"""


def test_get_chunks_start_index_negative():
    with raises(AssertionError):
        get_chunks(start_index=-1, end_index=1, chunk_size=1)


def test_get_chunks_start_index_greater_than_end_index():
    with raises(AssertionError):
        get_chunks(start_index=2, end_index=1, chunk_size=1)


def test_get_chunks_negative_chunk_size():
    with raises(AssertionError):
        get_chunks(start_index=1, end_index=2, chunk_size=-3)


def test_get_chunks_zero_chunk_size():
    with raises(AssertionError):
        get_chunks(start_index=1, end_index=2, chunk_size=0)


def test_get_chunks_same_indexes():
    chunks = get_chunks(start_index=1, end_index=1, chunk_size=2)
    assert len(chunks) == 1
    assert chunks[0].start_index == 1
    assert chunks[0].end_index == 1


"""Test output types"""


def test_get_chunks_output_type():
    chunks = get_chunks(start_index=0, end_index=2, chunk_size=2)
    assert isinstance(chunks, List)


def test_get_chunks_output_chunks_type():
    chunks = get_chunks(start_index=0, end_index=2, chunk_size=2)

    for chunk in chunks:
        assert isinstance(chunk, Chunk)


"""Test chunking"""


def test_get_chunks_chunking_base():
    chunks = get_chunks(start_index=0, end_index=5, chunk_size=2)
    assert len(chunks) == 3

    for chunk in chunks:
        assert len(chunk) == 2


def test_get_chunks_chunking_partial_last():
    chunks = get_chunks(start_index=0, end_index=6, chunk_size=2)
    assert len(chunks) == 4
    assert len(chunks[3]) == 1


def test_get_chunks_splitting_one_large_chunk():
    chunks = get_chunks(start_index=0, end_index=6, chunk_size=100)
    assert len(chunks) == 1
    assert len(chunks[0]) == 7
