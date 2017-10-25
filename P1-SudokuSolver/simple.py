rows = 'ABCDEFGHI'
cols = '123456789'

def cross(A, B):
    """
    "Cross product of elements in A and elements in B."
    """
    return [s+t for s in A for t in B]

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
forward_diagonal_units = [cross(r, c) for r, c in zip(rows, cols)]
backward_diagonal_units = [cross(r, c) for r, c in zip(rows, reversed(cols))]

print(forward_diagonal_units)
print(backward_diagonal_units)

