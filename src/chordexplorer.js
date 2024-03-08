import * as Chord from "tonal";

const defaultInversions = [
  [1, 2, 3, 4],
  [2, 3, 4, 5],
  [3, 4, 5, 6],
  [4, 5, 6, 7],
]
const defaultNotes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
const defaultChords = ["m", "M"]
const defaultOctaves = [2, 3, 4]

// Simple metric space on chords.Counts notes which belong to
// one chord but not the other.Octave - sensitive.
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
    let allChords = []
    for (let i = 0; i < roots.length; i++) {
      for (let j = 0; j < chords.length; j++) {
        for (let k = 0; k < octaves.length; k++) {
          let degrees = Chord.degrees(chords[j], roots[i] + octaves[k])
          for (let l = 0; l < inversions.length; l++) {
            let inversion = inversions[l]
            allChords.push(inversion.map(degrees))
          }
        }
      }
    }
  }

  nextChord(chord) {
    let possibles = []
    for (let i = 0; i < this.allChords.length; i++) {
      if (this.distance(chord, this.allChords[i]) < this.distance) {
        possibles.push(this.allChords[i])
      }
    }
    return possibles[Math.floor(Math.random() * possibles.length)]
  }
}

class DefaultChordExplorer extends ChordExplorer {
  constructor() {
    super(defaultInversions, defaultNotes, defaultChords, defaultOctaves, chordDistance)
  }
}

export { chordDistance, ChordExplorer, DefaultChordExplorer }
export default ChordExplorer