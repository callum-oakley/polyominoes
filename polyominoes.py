# A representation is a set of points corresponding to the location of each of
# the corresponding polyominoes constituent squares. A representation is
# normalized if the co-ordinates of all of its points are non-negative, at
# least one x co-ordinate is 0 and at least one y co-ordinate is 0.
def normalize(representation):
    dx = min(x for x, _ in representation)
    dy = min(y for _, y in representation)
    return frozenset((x - dx, y - dy) for x, y in representation)

# We'll store a polyomino as a set of the normalized representations of all its
# rotations and reflections.
def newPolyomino(representation):
    return frozenset(normalize(r) for r in [
        {( x,  y) for x, y in representation}, # identity
        {(-y,  x) for x, y in representation}, # rotate pi/2
        {(-x, -y) for x, y in representation}, # rotate pi
        {( y, -x) for x, y in representation}, # rotate 3pi/2
        {(-x,  y) for x, y in representation}, # reflect in x axis
        {( x, -y) for x, y in representation}, # reflect in y axis
        {( y,  x) for x, y in representation}, # reflect in y = x
        {(-y, -x) for x, y in representation}, # reflect in y = -x
    ])

# It's useful to be able to get a single representation for a given polyomino.
def represent(polyomino):
    return set(next(iter(polyomino)))

# We can build (n + 1)-ominoes by adding squares to n-ominoes
def grow(representation):
    return (newPolyomino(representation.union({s})) for s in {
        (x + dx, y + dy)
        for x, y in representation
        for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]
        if (x + dx, y + dy) not in representation
    })

# This is everything we need to generate the set of all n-ominoes...
def polyominoes(n):
    ominoes = {1: {newPolyomino({(0, 0)})}}
    for i in range(1, n):
        ominoes[i + 1] = {a for b in ominoes[i] for a in grow(represent(b))}
    return [represent(p) for p in ominoes[n]]
