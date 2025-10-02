from dataclasses import dataclass


class DimensionMismatchError(Exception):
    """Raised when vectors do not have the same dimension (length)."""

    pass


@dataclass
class Vector:
    values: list[float]

    def dim(self):
        return len(self.values)

    def __add__(self, vec):
        if isinstance(vec, Vector):
            if len(self.values) != len(vec.values):
                raise DimensionMismatchError(
                    f"Vectors must have the same demension got {len(self.values)} and {len(vec.values)}"
                )
            result: list[int] = []
            for item1, item2 in zip(self.values, vec.values):
                result.append(item1 + item2)

            return Vector(result)
        else:
            raise TypeError(
                f"Unsupported operand type(s) for +: 'Vector' and '{type(vec).__name__}'"
            )

    def scale(self, scaler: int):
        result: Vector = []
        for item in self.values:
            result.append(scaler * item)
        return Vector(result)


#    @staticmethod
#    def is_independent(vectors: list[Vector]) -> bool:
#        """
#        Linear independance is defined as a set of .vavectors that are
#        not a linear combinaition of other.
#        """
#        pass
#
#    @staticmethod
#    def gausin_elmination(matrix: list[Vector]) -> list[Vector]:
#        pass
