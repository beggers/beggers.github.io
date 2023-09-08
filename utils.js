export function wrapInSpans(text, c) {
    return `<span class=${c}>${text}</span>`
}

export const randBetweenIntegers = function(min, max) {
    return Math.floor(rand() * (max - min)) + min;
}

export var seed = 10;
console.log(seed);

export var rand = mulberry32(seed);

// We can't seed Math.random().
function mulberry32(a) {
    return function() {
      var t = seed += 0x6D2B79F5;
      t = Math.imul(t ^ t >>> 15, t | 1);
      t ^= t + Math.imul(t ^ t >>> 7, t | 61);
      return ((t ^ t >>> 14) >>> 0) / 4294967296;
    }
}
