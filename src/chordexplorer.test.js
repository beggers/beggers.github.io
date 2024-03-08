import { chordDistance } from './chordexplorer';

test('basic chord distance', () => {
  expect(chordDistance([0, 4, 7], [0, 4, 7])).toBe(0);
});