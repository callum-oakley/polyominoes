# A representation is a set of points corresponding to the location of each of
# the corresponding polyominoes constituent squares. A representation is
# normalized if the co-ordinates of all of its points are non-negative, at
# least one x co-ordinate is 0 and at least one y co-ordinate is 0.

def normalize(representation):
    dx = min(x for (x, _) in representation)
    dy = min(y for (_, y) in representation)
    return frozenset((x - dx, y - dy) for (x, y) in representation)

# It makes things easier later if we store a polyomino as a set of the
# normalized representations of all its rotations and reflections.

def polyomino(representation):
    transformations = [
        lambda s: ( s[0],  s[1]),
        lambda s: (-s[1],  s[0]),
        lambda s: (-s[0], -s[1]),
        lambda s: ( s[1], -s[0]),
        lambda s: (-s[0],  s[1]),
        lambda s: ( s[0], -s[1]),
        lambda s: ( s[1],  s[0]),
        lambda s: (-s[1], -s[0])
    ]
    return frozenset(
        normalize({t(s) for s in representation}) for t in transformations
    )
