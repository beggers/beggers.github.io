// A dumb chord class. Only utilities are to calculate the distance between two
// chords ignoring bass, and to hydrate a random bass note.
class Chord {
  constructor(notes) {
    this.notes = notes
  }

  distance(other) {
    let aSet = new Set(this.notes)
    let bSet = new Set(other.notes)

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

  withRandomBass(bassOctave) {
    let b = this.notes[Math.floor(Math.random() * this.notes.length)]
    b = b.substring(0, b.length - 1) + bassOctave
    return [...this.notes, b]
  }
}

export { Chord }
export default Chord