import { getSingleAnimal } from './animals.js';
import { Enclosure } from './enclosure.js';
import { getSaying } from './sayings.js';
import { randBetweenIntegers } from './utils.js';

const SAYING_MAX_LINE_LENGTH = 35;

// TODO dynamic canvas size?
const ENCLOSURE_HEIGHT = 40;
const ENCLOSURE_WIDTH = 125;
const PADDING_Y = 4;
const PADDING_X = 10;
const LINE_LENGTH = 5;

// This is ugly. This function returns an HTML <body> formatted as a string.
// It contains all the formatting needed to correctly display characters and colors,
// e.g. grass is wrappde with <span class="grass"></span>. The CSS classes
// themselves are defined in index.tl 🤢
export const getBody = function() {
    // We build the body up in four steps:
    // - Select the saying and the animal or animals that will say it.
    // - Create an empty string grid of the right size (our enclosure).
    // - Decide where everything goes.
    // - Insert items into the character array with formatting.
    //
    // Using a string grid makes life easier: we can insert formatting items
    // such as escapes and <span>s into the grid without effecting the length
    // of each line. We just need to make sure that the finished project renders
    // to one character per grid element.

    // TODO 2-person dialogues
    var enclosure = new Enclosure(ENCLOSURE_HEIGHT, ENCLOSURE_WIDTH);

    const saying = getSaying();
    const [animal, side] = getSingleAnimal();
    const [sayingInBubble, bubbleEndpoint] = formatSaying(saying[0], side, LINE_LENGTH);
    var [animalOffsetY, animalOffsetX] = calculateOffset(animal, bubbleEndpoint);

    var maxWidth = SAYING_MAX_LINE_LENGTH;
    for (var i = 0; i < animal.length ; i++) {
        if (animal[i].length > maxWidth) {
            maxWidth = animal[i].length;
        }
    }
    const [startY, startX] = getInitialPositionWithinBounds(
        ENCLOSURE_HEIGHT,
        ENCLOSURE_WIDTH,
        PADDING_Y,
        PADDING_X,
        animal.length + bubbleEndpoint[0], // not quite correct, who cares
        maxWidth
    );

    enclosure.copyInAtPosition(sayingInBubble, startY, startX, "bubble", true);
    enclosure.copyInAtPosition(animal, startY + animalOffsetY, startX + animalOffsetX, "animal", true);

    return (
`
<body>
    <pre>
${enclosure.getDisplayable()}
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

    // -2 for "right" is correct though unintuitive. One for zero-indexing, one for the fencepost.
    // For "left" they cancel each other out and we do -0.
    var bubbleXStart = animalSide === "right" ? connectingPoint + connectingLineLength - 2 : connectingPoint - connectingLineLength;
    return [finalLines, [finalLines.length - 1, bubbleXStart]];
}

// We need to do all this so that we can style (color) the speech bubble differently
// from the animal.
const calculateOffset = function(animal, bubbleEndpoint) {
    // This is inefficient but still fast enough and I'm tired and at the airport.
    for (var i = 0; i < animal.length; i++) {
        for (var j = 0; j < animal[i].length; j++) {
            var escapeCount = 0;
            if (animal[i][j] === "\\") {
                escapeCount += 1;
            }
            if (animal[i][j] === "ñ") {
                return [bubbleEndpoint[0] - i, bubbleEndpoint[1] - j - escapeCount / 2];
            }
        }
    }
}

const getInitialPositionWithinBounds = function(yMax, xMax, yPadding, xPadding, yWidth, xWidth) {
    return [
        randBetweenIntegers(yPadding, yMax - yPadding - yWidth),
        randBetweenIntegers(xPadding, xMax - xPadding - xWidth)
    ];
}