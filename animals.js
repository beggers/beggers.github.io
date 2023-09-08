import { randBetweenIntegers } from './utils.js';

export const getSingleAnimal = function() {
    const choice = animals[randBetweenIntegers(0, animals.length)]
    return choice;
}

// from cowsay
const cowRight = [
"  ^__^",
"ñ (oo)\\_______",
"  (__)\\       )\\/\\",
"      ||----w |",
"      ||     ||"
]

// http://www.ascii-art.de/ascii/t/turkey.txt
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

// http://www.ascii-art.de/ascii/t/turkey.txt
const turkeyLeft = [
"                     .--.",
"    {\\             / q {\\ ñ",
"    { `\\           \\ (-(~`",
"   { '.{`\\          \\ \\ )",
"   {'-{ ' \\  .-\"\"'-. \\ \\",
"   {._{'.' \\/       '.) \\",
"   {_.{.   {`            |",
"   {._{ ' {   ;'-=-.     |",
"    {-.{.' {  ';-=-.`    /",
"     {._.{.;    '-=-   .'",
"      {_.-' `'.__  _,-'",
"               |||`",
"              .='==,",
]

// We repeat ourselves a little here but it's easier than normalizing probabilities.
const animals = [
    [cowRight, "right"],
    [turkeyRight, "right"],
    [turkeyLeft, "left"]
]