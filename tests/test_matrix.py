from linalg.matrix import Matrix, rref
from linalg.vector import Vector

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


def to_rows(M):  # helper for assertions
    return M[0] if isinstance(M, tuple) else M


def test_rref_identity():
    A = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    R, piv = rref(A, exact=True)
    assert R == A
    assert piv == [0, 1, 2]


def test_rref_simple():
    A = [[1, 2], [3, 4]]
    R, piv = rref(A, exact=True)
    assert R == [[1, 0], [0, 1]]
    assert piv == [0, 1]


def test_rref_rank_deficient():
    A = [[1, 2, 3], [2, 4, 6]]  # second row = 2*first
    R, piv = rref(A, exact=True)
    assert piv == [0]
    # RREF should be [[1,2,3],[0,0,0]] after reduction
    assert R[1] == [0, 0, 0]


def test_rref_float_tolerance():
    A = [[1e-14, 1.0], [0.0, 1.0]]
    R, piv = rref(A, exact=False, tol=1e-12)
    # the tiny 1e-14 should be treated as zero; pivot in col 1 only
    assert piv == [1]


# def test_rref_one_vec_in_row_one():
#    vectors = Vector([1, 0, 0])
#    uut = Matrix(vectors)
#    expected = Matrix(Vector([1, 0, 0]))
#    assert expected == uut.rref()
