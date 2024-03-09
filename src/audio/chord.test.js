import { Chord } from './chord'

test('distance between a chord and itself should be zero', () => {
  let chord = new Chord(["C4", "E4", "G4"])
  expect(chord.distance(chord)).toBe(0)
})

test('chordDistance between a chord and itself with different order should be zero', () => {
  let chord = new Chord(["C4", "E4", "G4"])
  let transposition = new Chord(["E4", "G4", "C4"])
  expect(chord.distance(transposition)).toBe(0)
  expect(transposition.distance(chord)).toBe(0)
})

test('chordDistance between chords should be one if they have one note different', () => {
  let chord = new Chord(["C4", "E4"])
  let other = new Chord(["C4", "E4", "A4"])
  expect(chord.distance(other)).toBe(1)
  expect(other.distance(chord)).toBe(1)
})

test('withRandomBass always returns a bassified note from the chord', () => {
  let chord = new Chord(["C4", "E4", "G4"])
  for (let i = 0; i < 100; i++) {
    let bassified = chord.withRandomBass(2)

    expect(bassified.length).toBe(4)
    expect(bassified[3]).toMatch(/2$/)

    let tonic = bassified[bassified.length - 1].substring(0, bassified[0].length - 1)
    let found = false
    for (let note of bassified.slice(0, 3)) {
      if (note.substring(0, note.length - 1) == tonic) {
        found = true
        break
      }
    }
    expect(found).toBe(true)
  }
})

test('withRandomBass returns uniformly random bass notes', () => {
  let chord = new Chord(["C4", "E4", "G4"])
  let basses = {}
  for (let i = 0; i < 1000; i++) {
    let bassified = chord.withRandomBass(2)
    let bass = bassified[3]
    basses[bass] = (basses[bass] || 0) + 1
  }
  expect(Object.keys(basses).length).toBe(3)
  for (let bass in basses) {
    expect(basses[bass]).toBeGreaterThan(200)
  }
})