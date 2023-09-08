import { randBetweenIntegers } from './utils.js';

export const getAnimal = function() {
    const choice = animals[randBetweenIntegers(0, animals.length)]
    return choice;
}

// from cowsay
const cowLeftFacing = [
"  ^__^",
"ñ (oo)\\_______",
"  (__)\\       )\\/\\",
"      ||----w |",
"      ||     ||"
]

// from cowsay (reversed)
const cowRightFacing = [
"            ^__^",
"    _______/(oo) ñ",
"\\/\\(       /(__)",
"   | w----||",
"   ||     ||",
]

// http://www.ascii-art.de/ascii/t/turkey.txt
const turkeyLeftFacing = [
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
const turkeyRightFacing = [
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
    [cowRightFacing, "right"],
    [turkeyRightFacing, "right"],
    [turkeyLeftFacing, "left"],
    [cowLeftFacing, "left"],
]