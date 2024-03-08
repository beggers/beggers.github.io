'use strict'
import { chordDistance } from './chordexplorer.js';

test('distance between a chord and itself should be zero', () => {
  let chord = ["C4", "E4", "G4"]
  expect(chordDistance(chord, chord)).toBe(0)
})

test('distance between a chord and itself with different order should be zero', () => {
  let chord = ["C4", "E4", "G4"]
  let transposition = ["E4", "G4", "C4"]
  expect(chordDistance(chord, transposition)).toBe(0)
  expect(chordDistance(transposition, chord)).toBe(0)
})

test('distance between chords should be one if they have one note different', () => {
  let chord = ["C4", "E4"]
  let other = ["C4", "E4", "A4"]
  expect(chordDistance(chord, other)).toBe(1)
  expect(chordDistance(other, chord)).toBe(1)
})

