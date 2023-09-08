import { getAnimal } from './animals.js';
import { Enclosure } from './enclosure.js';
import { getNSayings } from './sayings.js';
import { randBetweenIntegers } from './utils.js';

const SAYING_MAX_LINE_LENGTH = 35;

// TODO dynamic canvas size?
const ENCLOSURE_HEIGHT = 40;
const ENCLOSURE_WIDTH = 120;
const PADDING_Y = 2;
const PADDING_X = 5;
const LINE_LENGTH = 3;
const MAX_PLACEMENT_TRIES = 5;

// This is ugly. This function returns an HTML <body> formatted as a string.
// It contains all the formatting needed to correctly display characters and colors,
// e.g. grass is wrappde with <span class="grass"></span>. The CSS classes
// themselves are defined in index.tl 🤢
export const getBody = function(userAgent) {
    if (userAgent.match(/Android/i)
    || userAgent.match(/webOS/i)
    || userAgent.match(/iPhone/i)
    || userAgent.match(/iPad/i)
    || userAgent.match(/iPod/i)
    || userAgent.match(/BlackBerry/i)
    || userAgent.match(/Windows Phone/i)) {
        return (
    // State-of-the-art mobile support
`
<body>
    <pre>
      <span class="bubble">  _______________________________</span> 
      <span class="bubble">/</span> <span class="dialogue">ben eggers dot com (visit us on </span><span class="bubble">\\</span>
      <span class="bubble">\\</span> <span class="dialogue">desktop!)</span>                       <span class="bubble">/</span>
      <span class="bubble">  -------------------------------</span> 
            <span class="bubble">\\</span>   <span class="animal">^__^</span>
            <span class="bubble"> \\</span>  <span class="animal">(oo)\\_______<span>
                <span class="animal">(__)\\       )\\/\\</span>
                    <span class="animal">||----w |</span>
                    <span class="animal">||     ||</span>
    </pre>
</body>
`
        )
    }
    var enclosure = new Enclosure(ENCLOSURE_HEIGHT, ENCLOSURE_WIDTH);
    var rectsToAvoid = []; // [y, x, height, width]

    //const numAnimals = randBetweenIntegers(1, 3);
    const numAnimals = 2
    const sayings = getNSayings(numAnimals);
    for (var i = 0; i < numAnimals; i++) {
        const saying = sayings[i];

        const [animal, side] = getAnimal();
        const [sayingInBubble, bubbleEndpoint] = formatSaying(saying, side, LINE_LENGTH);
        var [animalOffsetY, animalOffsetX] = calculateOffset(animal, bubbleEndpoint);

        // Dimensions (upper bounds) for the rect containing our animal + bubble.
        var heightUpperBound = animal.length + bubbleEndpoint[0];
        const leftOffset = Math.max(0, -1 * animalOffsetX);
        var maxLength = 0;
        for (var i = 0; i < animal.length; i++) {
            if (animal[i].length > maxLength) {
                maxLength = animal[i].length;
            }
        }
        const rightOffset = maxLength + Math.max(0, animalOffsetX);

        var startY, startX;
        for (var j = 0; j < MAX_PLACEMENT_TRIES; j++) {
            [startY, startX] = getInitialPositionWithinBounds(
                ENCLOSURE_HEIGHT,
                ENCLOSURE_WIDTH,
                PADDING_Y,
                PADDING_X,
                heightUpperBound,
                leftOffset,
                rightOffset
            );
            for (var k = 0; k < rectsToAvoid.length; k++) {
                
            }
        }

        enclosure.draw(sayingInBubble, startY, startX, "bubble", true);
        enclosure.draw(animal, startY + animalOffsetY, startX + animalOffsetX, "animal", true);
    }

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
    // Need this to prevent the line from going out of bounds relative to the bubble width,
    // e.g. in the case of a very short saying.
    if (currentLine.length < connectingLineLength * 2) {
        const spaces = Math.ceil((connectingLineLength*2 - currentLine.length) / 2);
        currentLine = ' '.repeat(spaces) + currentLine + ' '.repeat(spaces);
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
    const connectingPoint = Math.round(maxLength / 2) + 1;
    const lineCharacter = animalSide === "left" ? "\\" : "/"
    for (var i = 0; i < connectingLineLength; i++) {
        var lineLocation = animalSide === "left" ? connectingPoint + i : connectingPoint - i;
        finalLines.push(' '.repeat(Math.max(0, lineLocation - 1)) +
                        lineCharacter +
                        ' '.repeat(Math.max(0, maxLength - lineLocation)))
    }

    // -2 for right is correct though unintuitive. One for zero-indexing, one for the fencepost.
    // For left they cancel each other out and we do -0.
    var bubbleXStart = animalSide === "left" ? connectingPoint + connectingLineLength - 2 : connectingPoint - connectingLineLength;
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

// We need to pass x and y info differently because the origin (top-left of bubble) is always at y = 0, but
// will be at some non-zero x when the animal is a right-facing animal.
const getInitialPositionWithinBounds = function(yMax, xMax, yPadding, xPadding, yWidth, leftOffset, rightOffset) {
    return [
        randBetweenIntegers(yPadding, yMax - yPadding - yWidth),
        randBetweenIntegers(xPadding + leftOffset, xMax - xPadding - rightOffset)
    ];
}