'use strict'
import { ChordManager, DefaultChordManager, defaultDistance } from './chordmanager.js'
import * as c from './chord.js'

// TODO figure out why proptests were so slow and maybe bring them back.

test('ChordManager generates chords correctly', () => {
  let chord = new c.Chord(["C4", "E4", "G4"])
  let e = new ChordManager(
    [[0, 1, 2]],
    ["C"],
    ["M"],
    [4],
    0,
  )
  expect(chord.distance(e.startingChord())).toEqual(0)
  expect(e.allChords.length).toEqual(1)
})

test('ChordManager generates possible chords correctly', () => {
  let chord = new c.Chord(["C4", "E4", "G4"])
  let invertedChords = [
    new c.Chord(["C4", "E4", "G4"]),
    new c.Chord(["E4", "G4", "C5"]),
    new c.Chord(["G4", "C5", "E5"])
  ]
  let inversions = [
    [0, 1, 2],
    [1, 2, 3],
    [2, 3, 4]
  ]
  let e = new ChordManager(
    inversions,
    ["C"],
    ["^"],
    [4],
    2,
  )
  let possibles = e.possibleNextChords(chord)
  expect(possibles.length).toBe(1)
  expect(possibles[0].distance(invertedChords[1])).toBe(0)
})

test('ChordManager never generates the same chord', () => {
  let chord = new c.Chord(["C4", "E4", "G4"])
  let e = new ChordManager(
    [[0, 1, 2]],
    ["C"],
    ["M"],
    [4],
    1,
  )
  let next = e.nextChord(chord)
  expect(next).toBeUndefined()
})

test('ChordManager generates inversions of C major', () => {
  let chord = new c.Chord(["C4", "E4", "G4"])
  let invertedChords = [
    new c.Chord(["C4", "E4", "G4"]),
    new c.Chord(["E4", "G4", "C5"]),
    new c.Chord(["G4", "C5", "E5"])
  ]
  let inversions = [
    [0, 1, 2],
    [1, 2, 3],
    [2, 3, 4]
  ]
  let e = new ChordManager(
    inversions,
    ["C"],
    ["M"],
    [4],
    2,
  )
  let freqs = {}
  for (let i = 0; i < 100; i++) {
    let next = e.nextChord(chord)
    expect(next).toBeDefined()
    let found = false
    for (let j = 0; j < invertedChords.length; j++) {
      if (invertedChords[j].distance(next) === 0) {
        freqs[invertedChords[j]] = (freqs[invertedChords[j]] || 0) + 1
        found = true
        break
      }
    }
    expect(found).toBe(true)
  }
  for (let j = 0; j < inversions.length; j++) {
    expect(freqs[invertedChords[j]]).toBeGreaterThan(20)
  }
})

test('DefaultChordManager always generates chords defaultDistance away', () => {
  let e = new DefaultChordManager()
  let chord = e.allChords[0]
  for (let i = 0; i < 1000; i++) {
    let next = e.nextChord(chord)
    expect(next).toBeDefined()

    const distance = chord.distance(next)
    expect(distance).not.toBe(0)
    expect(distance).toBeLessThanOrEqual(defaultDistance)
    chord = next
  }
})
