import * as Chord from "tonal";

// Simple metric space on chords. Counts notes which belong to
// one chord but not the other. Octave-sensitive.
const chordDistance = (a, b) => {
  let distance = 0
  for (let i = 0; i < a.length; i++) {
    if (!b.includes(a[i])) {
      distance++
    }
  }
  for (let i = 0; i < b.length; i++) {
    if (!a.includes(b[i])) {
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
    const inversions = [
      [1, 2, 3, 4],
      [2, 3, 4, 5],
      [3, 4, 5, 6],
      [4, 5, 6, 7],
    ]
    const notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    const allowedChords = ["m", "M"]
    const octaves = [2, 3, 4]
    super(inversions, notes, allowedChords, octaves, 1)
  }
}

export { chordDistance, ChordExplorer, DefaultChordExplorer }
export default ChordExplorer