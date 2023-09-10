export function wrapInSpans(text, c) {
    return `<span class=${c}>${text}</span>`
}

export const randBetweenIntegers = function(min, max) {
    return Math.floor(rand() * (max - min)) + min;
}

export var seed = Math.random();

export var rand = mulberry32(seed);

// We can't seed Math.random().
function mulberry32(a) {
    return function() {
      var t = a += 0x6D2B79F5;
      t = Math.imul(t ^ t >>> 15, t | 1);
      t ^= t + Math.imul(t ^ t >>> 7, t | 61);
      const r = ((t ^ t >>> 14) >>> 0) / 4294967296;
      return r;
    }
}

export function rectsOverlap(rect1, rect2) {
    // y, x, height, width
    const overlap = (
        (rect2[0] >= rect1[0] && rect2[0] <= rect1[0] + rect1[2]) ||
        (rect1[0] >= rect2[0] && rect1[0] <= rect2[0] + rect2[2])
    ) && (
        (rect2[1] >= rect1[1] && rect2[1] <= rect1[1] + rect1[3]) ||
        (rect1[1] >= rect2[1] && rect1[1] <= rect2[1] + rect2[3])
    )
    return overlap;
}

export function anyRectsOverlap(rects) {
    for (var i = 0; i < rects.length; i++) {
        for (var j = i + 1; j < rects.length; j++) {
            if (rectsOverlap(rects[i], rects[j])) {
                return true;
            }
        }
    }
    return false;
}