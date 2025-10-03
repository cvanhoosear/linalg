from linalg.vector import Vector
from linalg.dimension_mismatch_error import DimensionMismatchError

from typing import Final
import pytest


def test_zero_dim():
    vec = Vector([])
    assert 0 == vec.dim()


def test_three_dim():
    assert 3 == Vector([1, 2, 3]).dim()


def test_add_zero_vector():
    vec1 = Vector([0, 0, 0])
    vec2 = Vector([1, 2, 3])
    expected: Final[Vector] = Vector([1, 2, 3])
    assert expected == vec1 + vec2


def test_add():
    vec1 = Vector([1, 0, 0])
    vec2 = Vector([1, 2, 3])
    expected: Final[Vector] = Vector([2, 2, 3])
    assert expected == vec1 + vec2


def test_add_negative():
    vec1 = Vector([1, -2, 1])
    vec2 = Vector([1, 2, 3])
    expected: Final[Vector] = Vector([2, 0, 4])
    assert expected == vec1 + vec2


def test_vector_add_different_dimension():
    vec1 = Vector([1, -2, 1])
    vec2 = Vector([1, 2, 3, 4])
    with pytest.raises(DimensionMismatchError):
        vec1 + vec2


def test_vector_add_type_mismatch():
    with pytest.raises(TypeError):
        Vector([1, 2]) + 2


def test_vector_scale_with_zero():
    s = 0
    vec = Vector([2, 3, 4])
    expected: Final[Vector] = Vector([0, 0, 0])
    assert expected == vec.scale(s)


def test_vector_scale_ten():
    s = 10
    vec = Vector([2, 3, 4])
    expected: Final[Vector] = Vector([20, 30, 40])
    assert expected == vec.scale(s)


def test_vector_scale_negative_scaler():
    s = -1
    vec = Vector([2, 3, 4])
    expected: Final[Vector] = Vector([-2, -3, -4])
    assert expected == vec.scale(s)
