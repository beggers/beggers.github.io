import { Chord } from "tonal";

const defaultInversions = [
  [1, 2, 3, 4],
  [2, 3, 4, 5],
  [3, 4, 5, 6],
  [4, 5, 6, 7],
]
const defaultNotes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
const defaultChords = ["m", "M"]
const defaultOctaves = [2, 3, 4]
let defaultDistance = 2

// Simple metric space on chords.Counts notes which belong to
// one chord but not the other.Octave - sensitive.
// TODO this should be levenstein distance.
const chordDistance = (a, b) => {
  let aSet = new Set(a)
  let bSet = new Set(b)

  let distance = 0
  for (let note of aSet) {
    if (!bSet.has(note)) {
      distance++
    }
  }
  for (let note of bSet) {
    if (!aSet.has(note)) {
      distance++
    }
  }
  return distance
}

class ChordExplorer {
  constructor(inversions, roots, chords, octaves, distance) {
    this.inversions = inversions
    this.roots = roots
    this.chords = chords
    this.octaves = octaves
    this.distance = distance

    // TODO this could be a much more clever data structure.
    // But linear scanning is probably fine.
    this.allChords = []
    for (let i = 0; i < roots.length; i++) {
      for (let j = 0; j < chords.length; j++) {
        for (let k = 0; k < octaves.length; k++) {
          let degrees = Chord.steps(chords[j], roots[i] + octaves[k])
          for (let l = 0; l < inversions.length; l++) {
            let inversion = inversions[l]
            this.allChords.push(inversion.map(degrees))
          }
        }
      }
    }
  }

  possibleNextChords(chord) {
    let possibles = []
    for (let i = 0; i < this.allChords.length; i++) {
      if (chordDistance(chord, this.allChords[i]) === this.distance) {
        possibles.push(this.allChords[i])
      }
    }
    return possibles
  }

  nextChord(chord) {
    let possibles = this.possibleNextChords(chord)
    return possibles[Math.floor(Math.random() * possibles.length)]
  }
}

class DefaultChordExplorer extends ChordExplorer {
  constructor() {
    super(defaultInversions, defaultNotes, defaultChords, defaultOctaves, defaultDistance)
  }
}

export { chordDistance, ChordExplorer, DefaultChordExplorer, defaultDistance }
export default ChordExplorer