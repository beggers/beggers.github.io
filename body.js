import { getSingleAnimal } from './animals.js';
import { Canvas } from './canvas.js';
import { getSaying } from './sayings.js';
import { wrapInSpans } from './utils.js';

const SAYING_MAX_LINE_LENGTH = 35;

// TODO dynamic canvas size?
const CANVAS_HEIGHT = 50;
const CANVAS_WIDTH = 150;
const PADDING = 10;

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
    var canvas = new Canvas(CANVAS_HEIGHT, CANVAS_WIDTH);

    const saying = getSaying();
    const [animal, side] = getSingleAnimal();
    const [sayingInBubble, bubbleEndpoint] = formatSaying(saying[0], side, 5);
    var [animalOffsetY, animalOffsetX] = calculateOffset(animal, bubbleEndpoint);

    var maxWidth = SAYING_MAX_LINE_LENGTH;
    for (var i = 0; i < animal.length ; i++) {
        if (animal[i].length > maxWidth) {
            maxWidth = animal[i].length;
        }
    }
    const [startY, startX] = getInitialPositionWithinBounds(
        CANVAS_HEIGHT,
        CANVAS_WIDTH,
        PADDING,
        animal.length + bubbleEndpoint[0], // not quite correct, who cares
        maxWidth
    );

    canvas.copyInAtPosition(sayingInBubble, startY, startX, "bubble");
    canvas.copyInAtPosition(animal, startY + animalOffsetY, startX + animalOffsetX, "animal");

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
const formatSaying = function(s, animalSide, connectingLineLength) {
    var lines = [];
    const words = s.split(' ');

    // Break the saying up into lines of suitable length.
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

    // Compute the max length and make the string for the top and bottom of the bubble.
    const maxLength = Math.max(...(lines.map(l => l.length)));
    const topAndBottom = "  " + ("-").repeat(maxLength) + "  ";

    // Put it all together to make the bubble and put the words inside it, with
    // each word line padded to the same length.
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

    // And finally, the line connecting the bubble to the mouth.
    const connectingPoint = Math.round(maxLength / 3 * (animalSide === "right" ? 1 : 2))
    const lineCharacter = animalSide === "right" ? "\\" : "/"
    for (var i = 0; i < connectingLineLength; i++) {
        var lineLocation = animalSide === "right" ? connectingPoint + i : connectingPoint - i;
        finalLines.push(' '.repeat(lineLocation - 1) + lineCharacter + ' '.repeat(maxLength - lineLocation))
    }

    // [..., [... - 1, ... - 2]] is correct though unintuitive. One for zero-indexing, one for the fencepost.
    return [finalLines, [finalLines.length - 1, connectingPoint + connectingLineLength - 2]];
}

// We need to do all this so that we can style (color) the speech bubble differently
// from the animal.
const calculateOffset = function(animal, bubbleEndpoint) {
    // This is inefficient but still fast enough and I'm tired and at the airport.
    for (var i = 0; i < animal.length; i++) {
        for (var j = 0; j < animal[i].length; j++) {
            if (animal[i][j] === "ñ") {
                return [bubbleEndpoint[0] - i, bubbleEndpoint[1] - j];
            }
        }
    }
}

const getInitialPositionWithinBounds = function(yMax, xMax, padding, yWidth, xWidth) {
    return [
        randBetweenIntegers(padding, yMax - padding - yWidth),
        randBetweenIntegers(padding, xMax - padding - xWidth)
    ];
}
const randBetweenIntegers = function(min, max) {
    return Math.floor(Math.random() * (max - min)) + min;
}