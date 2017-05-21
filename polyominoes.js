const transformations = [
  ([ x, y ]) => [  x,  y ], // identity
  ([ x, y ]) => [ -y,  x ], // rotate pi/2
  ([ x, y ]) => [ -x, -y ], // rotate pi
  ([ x, y ]) => [  y, -x ], // rotate 3pi/2
  ([ x, y ]) => [ -x,  y ], // reflect in x axis
  ([ x, y ]) => [  x, -y ], // reflect in y axis
  ([ x, y ]) => [  y,  x ], // reflect in x = y
  ([ x, y ]) => [ -y, -x ]  // reflect in x = -y
];

class Polyomino {
  // Reduces a representation of a polyomino to a string such that two
  // representations of the same polyomino (up to translation) will produce the
  // same string
  static normalize(representation) {
    const dx = Math.min(...representation.map(([ x, y ]) => x));
    const dy = Math.min(...representation.map(([ x, y ]) => y));
    // Make the co-ordinates as small as possible, while all still positive
    const normalized = representation.map(([ x, y ]) => [ x - dx, y - dy ])
    return JSON.stringify(normalized.sort());
  }

  constructor(representation) {
    // Store a set of the normalized representations of each rotation and
    // reflection of the polyomino
    this.representations = new Set(
      transformations.map(t => representation.map(square => t(square)))
        .map(Polyomino.normalize)
    );
  }

  // Tests if the polyomino is represented by the provided list of squares
  isRepresentedBy(representation) {
    return this.representations.has(Polyomino.normalize(representation));
  }

  // Gets an arbitrary represenation of the polyomino
  get representation() {
    return JSON.parse(this.representations.values().next().value);
  }
}

const directions = [ [ 1, 0 ], [ 0, 1 ], [ -1, 0 ], [ 0, -1 ] ];

function containsSquare(representation, square) {
  return representation.some(s => JSON.stringify(s) === JSON.stringify(square));
}

// Returns an iterable of representations that can be built by adding one
// square to the given representation
function* grow(representation) {
  for ([ x, y ] of representation) {
    for ([ dx, dy ] of directions) {
      if (!containsSquare(representation, [ x + dx, y + dy ])) {
        yield [ ...representation, [ x + dx, y + dy ] ];
      }
    }
  }
}

// Tests if the provided representation corresponds to one of the provided
// polyominoes
function alreadyRepresented(polyominoes, representation) {
  return polyominoes.some(p => p.isRepresentedBy(representation));
}

// Returns an array of all free n-ominoes
function polyominoes(n) {
  const ominoes = { 1: [ new Polyomino([ [ 0, 0 ] ]) ] };
  for (let i = 2; i <= n; i++) {
    ominoes[i] = [];
    for (omino of ominoes[i - 1]) {
      for (representation of grow(omino.representation)) {
        if (!alreadyRepresented(ominoes[i], representation)) {
          ominoes[i].push(new Polyomino(representation));
        }
      }
    }
  }
  return ominoes[n];
}

module.exports = polyominoes;

// # Usage examples
//
// Find out how many 8-ominoes there are:
//
//     polyominoes(8).length;
//
// Get an array consisting of a single representation for each of them:
//
//     polyominoes(8).map(p => p.representation);
