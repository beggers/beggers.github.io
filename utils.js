export function wrapInSpans(text, c) {
    return `<span class=${c}>${text}</span>`
}

export const randBetweenIntegers = function(min, max) {
    return Math.floor(Math.random() * (max - min)) + min;
}
