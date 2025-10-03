from linalg.matrix import Matrix
from linalg.vector import Vector
from linalg.dimension_mismatch_error import DimensionMismatchError

import pytest


def test_init_empty():
    uut = Matrix()
    assert len(uut.matrix) == 0


def test_init_one_vector():
    vectors = [Vector([1, 0, 0])]
    uut = Matrix(vectors)
    assert len(uut.matrix) == 1
    assert uut.matrix == [[1], [0], [0]]


def test_init_three_vector():
    vectors = [Vector([1, 0, 0]), Vector([0, 1, 0]), Vector([0, 0, 1])]
    expected = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    uut = Matrix(vectors)
    assert len(uut.matrix) == len(expected)
    assert uut.matrix == expected


def test_init_vector_size_mismatch():
    vectors = [Vector([1, 0, 0]), Vector([0, 1, 0]), Vector([0, 1])]
    with pytest.raises(DimensionMismatchError):
        uut = Matrix(vectors)


def test_rref_one_vec_in_row_one():
    vectors = [Vector([1, 0, 0])]
    uut = Matrix(vectors)
    expected = Matrix(Vector([1, 0, 0]))
    assert expected == uut.rref()


def test_eq_other_not_a_matrix():
    vectors = [Vector([1, 0, 0])]
    uut = Matrix(vectors)
    assert 8 != uut


def test_eq_reflexivity():
    vectors = [Vector([1, 0, 0])]
    uut = Matrix(vectors)
    assert uut == uut
    assert uut != uut
