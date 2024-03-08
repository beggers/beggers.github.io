import { chordDistance } from './chordexplorer';
import fc from 'fast-check';

test('distance from equal chords should always be zero', () => {
  fc.assert(
    fc.property(fc.array(fc.string()), (chord) => {
      expect(chordDistance(chord, chord)).toBe(0);
    })
  );
});

test('distance should be symmetric', () => {
  fc.assert(
    fc.property(fc.array(fc.string()), fc.array(fc.string()), (a, b) => {
      expect(chordDistance(a, b)).toBe(chordDistance(b, a));
    })
  );
});