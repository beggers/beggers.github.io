import { Chord } from "tonal";
import * as c from './chord'

const defaultInversions = [
  // TODO some chord shapes which cross octaves?
  [1, 2, 3, 4],
  [2, 3, 4, 5],
  [3, 4, 5, 6],
  [4, 5, 6, 7],
]
const defaultNotes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
const defaultChords = ["^", "m", "Maj7", "m7"]
const defaultOctaves = [3, 4, 5]
let defaultDistance = 2

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
            this.allChords.push(new c.Chord(inversion.map(degrees)))
          }
        }
      }
    }
  }

  startingChord() {
    return this.allChords[0]
  }

  possibleNextChords(chord) {
    let possibles = []
    for (let i = 0; i < this.allChords.length; i++) {
      const distance = chord.distance(this.allChords[i])
      if (distance !== 0 && distance <= this.distance) {
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

export { ChordExplorer, DefaultChordExplorer, defaultDistance }
export default ChordExplorer