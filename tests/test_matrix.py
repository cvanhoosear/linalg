from linalg.matrix import Matrix
from linalg.vector import Vector
from linalg.dimension_mismatch_error import DimensionMismatchError

import pytest


def test_init_empty():
    with pytest.raises(ValueError):
        Matrix()


def test_init_one_vector():
    uut = Matrix(Vector([1, 0, 0]))
    assert uut.rows == [[1], [0], [0]]


def test_init_three_vector():
    expected = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    uut = Matrix(Vector([1, 0, 0]), Vector([0, 1, 0]), Vector([0, 0, 1]))
    assert uut.rows == expected


def test_init_vector_size_mismatch():
    with pytest.raises(ValueError):
        Matrix(Vector([1, 0, 0]), Vector([0, 1, 0]), Vector([0, 1]))


def test_eq_other_not_a_matrix():
    vectors = Vector([1, 0, 0])
    uut = Matrix(vectors)
    assert 8 != uut


def test_eq_reflexivity():
    vectors = Vector([1, 0, 0])
    uut = Matrix(vectors)
    assert uut == uut


# def test_rref_one_vec_in_row_one():
#    vectors = Vector([1, 0, 0])
#    uut = Matrix(vectors)
#    expected = Matrix(Vector([1, 0, 0]))
#    assert expected == uut.rref()
