import { getAnimal } from './animals.js';
import { Enclosure } from './enclosure.js';
import { getNSayings } from './sayings.js';
import { rand, randBetweenIntegers, anyRectsOverlap } from './utils.js';

const SAYING_MAX_LINE_LENGTH = 35;

// TODO dynamic canvas size?
const ENCLOSURE_HEIGHT = 45;
const ENCLOSURE_WIDTH = 150;
const PADDING_Y = 2;
const PADDING_X = 5;
const LINE_LENGTH = 3;
const MAX_PLACEMENT_TRIES = 10;
const TWO_ANIMAL_PROBABILITY = 0.2;

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
    var animals = [];

    const numAnimals = rand() <= TWO_ANIMAL_PROBABILITY ? 2 : 1;
    const sayings = getNSayings(numAnimals);

    // Get animals and sayings; format sayings for the animals.
    for (var i = 0; i < numAnimals; i++) {
        const saying = sayings[i];
        const [animal, direction] = getAnimal();
        const [sayingInBubble, bubbleEndpoint] = formatSaying(saying, direction, LINE_LENGTH);
        const [animalOffsetY, animalOffsetX] = calculateOffset(animal, bubbleEndpoint);
        animals.push([sayingInBubble, animal, animalOffsetY, animalOffsetX])
    }

    // Figure out where to place them.
    var rects = []; // [y, x, height, width]
    // Different from rects, since the starting placement point is the top-left of the bubble
    // and rect needs to hold the entire animal+bubble for collision detection. placementPoints
    // should be computable from the info in rects and animals but the code is gross.
    var placementPoints = []; // [y, x, height, width]
    for (var i = 0; i < MAX_PLACEMENT_TRIES; i++) {
        rects = [];
        placementPoints = [];
        for (var j = 0; j < animals.length; j++) {
            const [sayingInBubble, animal, animalOffsetY, animalOffsetX] = animals[j];

            // Dimensions for the rect containing our animal + bubble.
            const height = sayingInBubble.length + animal.length;
            const leftOffset = Math.max(0, -1 * animalOffsetX);
            // Haha code duplication ha ha.
            var maxLength = 0;
            for (var k = 0; k < sayingInBubble.length; k++) {
                if (sayingInBubble[k].length > maxLength) {
                    maxLength = sayingInBubble[k].length;
                }
            }
            for (var k = 0; k < animal.length; k++) {
                if (animal[k].length > maxLength) {
                    maxLength = animal[k].length;
                }
            }
            const rightOffset = maxLength + Math.max(0, animalOffsetX);

            const [startY, startX] = getRandomRectPositionWithinBounds(
                ENCLOSURE_HEIGHT,
                ENCLOSURE_WIDTH,
                PADDING_Y,
                PADDING_X,
                height,
                leftOffset,
                rightOffset
            );

            var rect = [startY, startX - leftOffset, height, leftOffset + rightOffset]
            rects.push(rect);
            placementPoints.push([startY, startX]);
        }

        if (!anyRectsOverlap(rects)) {
            break;
        } else if (i === MAX_PLACEMENT_TRIES - 1) {
            animals = [];
            rects = [];
            placementPoints = [];
        }
    }

    // Place them.
    for (var i = 0; i < animals.length; i++) {
        const [sayingInBubble, animal, animalOffsetY, animalOffsetX] = animals[i];
        const [startY, startX] = placementPoints[i];
        enclosure.draw(sayingInBubble, startY, startX, "bubble", true);
        enclosure.draw(animal, startY + animalOffsetY, startX + animalOffsetX, "animal", true);
    }

    return (
`
<body>
    <button onClick="window.location.reload();" onMouseDown="this.className='pressed'">
    <pre>  + -------------- +
  |   <span class="dialogue">Regenerate</span>   |
  + -------------- +</pre>
    </button>
    <pre>
${enclosure.getDisplayable()}
    </pre>
</body>
`
    )
}

// Returns the saying formatted inside a bubble with a speech line of connectingLineLength.
// Also returns the point [y, x] within the returned []string where the speech bubble
// ends so it can be lined up with the animal's ñ.
const formatSaying = function(s, animalDirection, connectingLineLength) {
    // TODO split return into [text, bubble] so we can color them differently.
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
    const lineCharacter = animalDirection === "left" ? "\\" : "/"
    for (var i = 0; i < connectingLineLength; i++) {
        var lineLocation = animalDirection === "left" ? connectingPoint + i : connectingPoint - i;
        finalLines.push(' '.repeat(Math.max(0, lineLocation - 1)) +
                        lineCharacter +
                        ' '.repeat(Math.max(0, maxLength - lineLocation)))
    }

    // -2 for left-facing is correct though unintuitive. One for zero-indexing, one for the fencepost.
    // For right-facing they cancel each other out and we do -0.
    var bubbleXStart = animalDirection === "left" ? connectingPoint + connectingLineLength - 2 : connectingPoint - connectingLineLength;
    return [finalLines, [finalLines.length - 1, bubbleXStart]];
}

// Calculate the [y, x] offset where the animal should be drawn relative to the bubble.
// y will always be positive, x may be negative.
const calculateOffset = function(animal, bubbleEndpoint) {
    // We need to do all this so that we can style (color) the speech bubble differently
    // from the animal.

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
const getRandomRectPositionWithinBounds = function(yMax, xMax, yPadding, xPadding, height, leftOffset, rightOffset) {
    // Todo this function doesn't need to accept so many arguments
    return [
        randBetweenIntegers(yPadding, yMax - yPadding - height),
        randBetweenIntegers(xPadding + leftOffset, xMax - xPadding - rightOffset)
    ];
}