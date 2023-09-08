import { randBetweenIntegers } from './utils.js';

const cowRight = [
"  ^__^",
"ñ (oo)\\_______",
"  (__)\\       )\\/\\",
"      ||----w |",
"      ||     ||"
]

const turkeyRight = [
"   .--.",
"ñ /} p \\             /}",
"  `~)-) /           /` }",
"   ( / /          /`}.' }",
"    / / .-'\"\"-.  / ' }-'}",
"   / (.'       \\/ '.'}_.}",
"  |            `}   .}._}",
"  |     .-=-';   } ' }_.}",
"   \\    `.-=-;'  } '.}.-}",
"    '.   -=-'    ;,}._.}",
"      `-,_  __.'` '-._}",
"          `|||",
"         .=='=,",
]

const animals = {
    "right": [
        cowRight,
        turkeyRight,
    ],
    "left": [

    ]
}

export const getSingleAnimal = function() {
    return [animals["right"][randBetweenIntegers(0, 2)], "right"];
}