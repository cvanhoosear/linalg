from .vector import Vector
from .dimension_mismatch_error import DimensionMismatchError
import copy


class Matrix:
    __hash__ = None

    def __init__(self, vectors: list[Vector] = []):
        self.matrix = [[]]
        if not vectors:
            pass
        # Verify vector are same length
        length = len(vectors[0])
        for vector in vectors:
            if length != len(vector):
                raise DimensionMismatchError

        # Transpose vectors
        return [[row[i] for row in matrix] for i in range(len(vectors))]

    def rref(self, tol: float = 1e-12) -> tuple["Matrix", list[int]]:
        a = copy.deepcopy(self.matrix)
        m = len(a)
        n = len
        return Matrix(Vector([1, 0, 0]))

    def __eq__(self, other) -> bool:
        if not isinstance(other, Matrix):
            return NotImplemented
        return self.matrix == other.matrix
