# A representation is a set of points corresponding to the location of each of
# the corresponding polyominoes constituent squares. A representation is
# normalized if the co-ordinates of all of its points are non-negative, at
# least one x co-ordinate is 0 and at least one y co-ordinate is 0.

def normalize(representation):
    dx = min(x for (x, _) in representation)
    dy = min(y for (_, y) in representation)
    return frozenset((x - dx, y - dy) for (x, y) in representation)

# We'll store a polyomino as a set of the normalized representations of all its
# rotations and reflections.

def newPolyomino(representation):
    transformations = [
        lambda s: ( s[0],  s[1]), # identity
        lambda s: (-s[1],  s[0]), # rotate pi/2
        lambda s: (-s[0], -s[1]), # rotate pi
        lambda s: ( s[1], -s[0]), # rotate 3pi/2
        lambda s: (-s[0],  s[1]), # reflect in x axis
        lambda s: ( s[0], -s[1]), # reflect in y axis
        lambda s: ( s[1],  s[0]), # reflect in y = x
        lambda s: (-s[1], -s[0])  # reflect in y = -x
    ]
    return frozenset(
        normalize({t(s) for s in representation}) for t in transformations
    )

# It's useful to be able to get a single representation for a given polyomino.

def represent(polyomino):
    return set(next(iter(polyomino)))

# We can build (n + 1)-ominoes by adding squares to n-ominoes

def grow(polyomino):
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    representation = represent(polyomino)
    for (x, y) in representation:
        for (dx, dy) in directions:
            if (x + dx, y + dy) not in representation:
                yield newPolyomino(representation.union({(x + dx, y + dy)}))

# This is everything we need to generate the set of all n-ominoes...

def polyominoes(n):
    ominoes = {1: {newPolyomino({(0, 0)})}}
    for i in range(1, n):
        ominoes[i + 1] = {a for b in ominoes[i] for a in grow(b)}
    return [represent(p) for p in ominoes[n]]

# Let's also provide a function to draw them, just for fun

def draw(representation):
    for x in range(len(representation)):
        for y in range(len(representation)):
            if (x, y) in representation:
                print("#", end=" ")
            else:
                print("·", end=" ")
        print()

# Or to draw the whole set

def drawBatch(representations):
    for r in representations:
        draw(r)
        print()
