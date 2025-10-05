from .vector import Vector

from typing import Sequence, Union
from fractions import Fraction

Number = Union[int, float, Fraction]


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

    @classmethod
    def from_rows(cls, rows: Sequence[Sequence[Number]]):
        # Build by columns so your Matrix invariant (columns as inputs) still holds
        if not rows:
            return cls([])  # or raise if you disallow empty
        # transpose rows -> columns
        cols = [[rows[i][j] for i in range(len(rows))] for j in range(len(rows[0]))]
        return cls(*cols)

    def rref(self, *, exact: bool = False, tol: float = 1e-12):
        R_rows, pivots = rref(self._rows, exact=exact, tol=tol)
        return Matrix.from_rows(R_rows), pivots

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


def rref(
    A: Sequence[Sequence[Number]], *, exact: bool = False, tol: float = 1e-12
) -> tuple[list[list[Number]], list[int]]:
    """
    Compute the Reduced Row Echelon Form (RREF) of matrix A.

    Args:
        A: m×n matrix as a sequence of row sequences.
        exact: if True, do exact rational arithmetic with Fraction.
               if False, do floating-point with tolerance 'tol'.
        tol: absolute tolerance for deciding numerical zeros (ignored if exact=True).

    Returns:
        R: RREF of A as a new list of rows (deep-copied).
        pivots: list of pivot column indices (in order of discovery).

    Properties of RREF R:
      - Each pivot (leading 1) is the only non-zero in its column.
      - Pivot rows are scaled so pivot == 1.
      - Rows of all zeros are at the bottom.
    """
    # Copy & coerce
    R = [list(row) for row in A]
    if not R:
        return [], []

    m = len(R)
    n = len(R[0])
    if any(len(row) != n for row in R):
        raise ValueError("All rows must have the same length")

    if exact:
        R = [[Fraction(x) for x in row] for row in R]

    pivots: List[int] = []
    r = 0  # current row we’re filling with a pivot
    for c in range(n):
        if r >= m:
            break

        # 1) Find pivot row: max |entry| below/at r (for stability in float mode)
        pivot_row = None
        best_val = Fraction(0) if exact else 0.0
        for i in range(r, m):
            val = R[i][c]
            mag = abs(val)
            if exact:
                is_nz = val != 0
                better = (pivot_row is None) or (mag > best_val)
            else:
                is_nz = mag > tol
                better = mag > best_val
            if is_nz and better:
                best_val = mag
                pivot_row = i

        # If no pivot in this column, continue to next column
        if pivot_row is None:
            continue

        # 2) Swap pivot row into position r
        if pivot_row != r:
            R[r], R[pivot_row] = R[pivot_row], R[r]

        # 3) Scale row r so that pivot entry becomes 1
        pivot = R[r][c]
        if exact:
            # Fraction division is exact
            R[r] = [x / pivot for x in R[r]]
        else:
            R[r] = [x / pivot for x in R[r]]

        # 4) Eliminate this column in all other rows
        for i in range(m):
            if i == r:
                continue
            factor = R[i][c]
            if exact:
                if factor != 0:
                    R[i] = [xi - factor * xrj for xi, xrj in zip(R[i], R[r])]
            else:
                if abs(factor) > tol:
                    R[i] = [xi - factor * xrj for xi, xrj in zip(R[i], R[r])]
                    # Zero-out tiny noise
                    R[i] = [0.0 if abs(xi) <= tol else xi for xi in R[i]]

        pivots.append(c)
        r += 1

    # Optional: clean tiny residuals in pivot rows for float mode
    if not exact:
        for i in range(m):
            R[i] = [0.0 if abs(x) <= tol else x for x in R[i]]

    return R, pivots
