import { getSingleAnimal } from './animals.js';
import { Canvas } from './canvas.js';
import { getSaying } from './sayings.js';
import { wrapInSpans } from './utils.js';

const SAYING_MAX_LINE_LENGTH = 35;

// This is ugly. This function returns an HTML <body> formatted as a string.
// It contains all the formatting needed to correctly display characters and colors,
// e.g. grass is wrappde with <span class="grass"></span>. The CSS classes
// themselves are defined in index.tl 🤢
export const getBody = function() {
    // We build the body up in four steps:
    // - Select the saying and the animal or animals that will say it.
    // - Create an empty string grid of the right size (our canvas).
    // - Decide where everything goes.
    // - Insert items into the character array with formatting.
    //
    // Using a string grid makes life easier: we can insert formatting items
    // such as escapes and <span>s into the grid without effecting the length
    // of each line. We just need to make sure that the finished project renders
    // to one character per grid element.

    // TODO 2-person dialogues
    const saying = getSaying().map((s) => formatSaying(s))[0];
    const animal = getSingleAnimal();
    // TODO dynamic canvas size?
    var canvas = new Canvas(25, 50);
    canvas.copyInAtPosition(saying, 5, 5, "bubble");

    return (
`
<body>
    <pre>
${canvas.getDisplayable()}
    </pre>
</body>
`
    )
}

// TODO split return into [text, bubble] so we can color them differently.
const formatSaying = function(s) {
    var lines = [];
    const words = s.split(' ');

    var currentLine = "";
    for (var i = 0; i < words.length; i++) {
        // This loop doesn't work if a word is longer than SAYING_MAX_LINE_LENGTH.
        if (currentLine.length + words[i].length > SAYING_MAX_LINE_LENGTH) {
            lines.push(currentLine);
            currentLine = "";
        }
        currentLine += (currentLine == "" ? "" : " ") + words[i];
    }
    lines.push(currentLine);

    const maxLength = Math.max(...(lines.map(l => l.length)));
    const topAndBottom = "  " + ("-").repeat(maxLength) + "  ";

    var finalLines = [];

    finalLines.push(topAndBottom);
    if (lines.length === 1) {
        finalLines.push("< " + lines[0] + " >");
    } else {
        for (var i = 0; i < lines.length; i++) {
            lines[i] += ' '.repeat(maxLength - lines[i].length);
            if (i === 0) {
                finalLines.push("/ " + lines[i] + " \\");
            } else if (i === lines.length - 1) {
                finalLines.push("\\ " + lines[i] + " /");
            } else {
                finalLines.push("| " + lines[i] + " |");
            }
        }
    }
    finalLines.push(topAndBottom);

    return finalLines;
}