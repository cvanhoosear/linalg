from .vector import Vector
from .dimension_mismatch_error import DimensionMismatchError
import copy


class Matrix:
    __hash__ = None

    def __init__(self, *vectors):
        if not vectors:
            raise ValueError("Matrix requires at least one Vector")
        if not (isinstance(v, Vector) for v in vectors):
            raise TypeError("All arguments must ve Vectors instances")

        processed = []
        for v in vectors:
            if isinstance(v, Vector):
                processed.append(v)
            elif isinstance(v, list) or isinstance(v, tuple):
                processed.append(Vector(v))
            else:
                raise TypeError(f"Invalid column type {type(v)}")

        length = len(processed[0])
        if any(len(v) != length for v in processed):
            raise ValueError("All vetors must have the same dimension")

        self._cols = [v.values[:] for v in processed]
        self._rows = [list(row) for row in zip(*self._cols)]

        # Dimensions
        self.nrows = len(self._rows)
        self.ncols = len(self._cols)

    @property
    def rows(self):
        return [r[:] for r in self._rows]

    @property
    def cols(self):
        return [c[:] for c in self._cols]

    def __repr__(self):
        return "Matrix([" + ",\n        ".join(str(r) for r in self._rows) + "])"

    def shape(self):
        return (self.nrows, self.ncols)

    def rref(self, tol: float = 1e-12) -> tuple["Matrix", list[int]]:
        a = copy.deepcopy(self.matrix)
        m = len(a)
        n = len
        return Matrix(Vector([1, 0, 0]))

    def __eq__(self, other):
        if not isinstance(other, Matrix):
            return NotImplemented
        if self.shape() != other.shape():
            return False

        tol = 1e-9
        for r1, r2 in zip(self._rows, other._rows):
            for a, b in zip(r1, r2):
                if abs(a - b) > tol:
                    return False
        return True
