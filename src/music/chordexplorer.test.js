'use strict'
import { chordDistance, ChordExplorer, DefaultChordExplorer, defaultDistance } from './chordexplorer.js';

// TODO figure out why proptests were so slow and maybe bring them back.

test('distance between a chord and itself should be zero', () => {
  let chord = ["C4", "E4", "G4"]
  expect(chordDistance(chord, chord)).toBe(0)
})

test('chordDistance between a chord and itself with different order should be zero', () => {
  let chord = ["C4", "E4", "G4"]
  let transposition = ["E4", "G4", "C4"]
  expect(chordDistance(chord, transposition)).toBe(0)
  expect(chordDistance(transposition, chord)).toBe(0)
})

test('chordDistance between chords should be one if they have one note different', () => {
  let chord = ["C4", "E4"]
  let other = ["C4", "E4", "A4"]
  expect(chordDistance(chord, other)).toBe(1)
  expect(chordDistance(other, chord)).toBe(1)
})

test('ChordExplorer generates chords correctly', () => {
  let chord = ["C4", "E4", "G4"]
  let e = new ChordExplorer(
    [[0, 1, 2]],
    ["C"],
    ["M"],
    [4],
    0,
  )
  expect(e.allChords).toEqual([chord])
})

test('ChordExplorer generates possible chords correctly', () => {
  let chord = ["C4", "E4", "G4"]
  let invertedChords = [
    ["C4", "E4", "G4"],
    ["E4", "G4", "C5"],
    ["G4", "C5", "E5"]
  ]
  let inversions = [
    [0, 1, 2],
    [1, 2, 3],
    [2, 3, 4]
  ]
  let e = new ChordExplorer(
    inversions,
    ["C"],
    ["M"],
    [4],
    2,
  )
  let possibles = e.possibleNextChords(chord)
  expect(possibles).toEqual([invertedChords[1]])
})

test('ChordExplorer never generates the same chord', () => {
  let chord = ["C4", "E4", "G4"]
  let e = new ChordExplorer(
    [[0, 1, 2]],
    ["C"],
    ["M"],
    [4],
    1,
  )
  let next = e.nextChord(chord)
  expect(next).toBeUndefined()
})

test('ChordExplorer generates inversions of C major', () => {
  let chord = ["C4", "E4", "G4"]
  let invertedChords = [
    ["C4", "E4", "G4"],
    ["E4", "G4", "C5"],
    ["G4", "C5", "E5"]
  ]
  let inversions = [
    [0, 1, 2],
    [1, 2, 3],
    [2, 3, 4]
  ]
  let e = new ChordExplorer(
    inversions,
    ["C"],
    ["M"],
    [4],
    2,
  )
  for (let i = 0; i < 100; i++) {
    let next = e.nextChord(chord)
    expect(next).toBeDefined()
    let found = false
    for (let j = 0; j < invertedChords.length; j++) {
      if (chordDistance(next, invertedChords[j]) === 0) {
        found = true
        break
      }
    }
    expect(found).toBe(true)
  }
})

test('DefaultChordExplorer always generates chords defaultDistance away', () => {
  let e = new DefaultChordExplorer()
  let chord = e.allChords[0]
  for (let i = 0; i < 1000; i++) {
    let next = e.nextChord(chord)
    expect(next).toBeDefined()
    expect(next).not.toEqual(chord)

    const distance = chordDistance(chord, next)
    expect(distance).not.toBe(0)
    expect(distance).toBeLessThanOrEqual(defaultDistance)
    chord = next
  }
})
