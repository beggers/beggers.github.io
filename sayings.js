import { rand } from './utils.js';

const MAX_TRIES = 5;

export const getNSayings = function(n) {
    var ret = [];
    for (var i = 0; i < n; i++) {
        for (var j = 0; j < MAX_TRIES; j++) {
            var s = getSaying();
            if (!ret.includes(s)) {
                ret.push(s);
                break;
            }
        }
    }
    return ret;
}

export const getSaying = function() {
    return sayings[sayings.length * rand() | 0]
}

// The sayings themselves. If the list has two items, it's a dialogue and needs
// two animals.
export const sayings = [
    "ok",
    "ben eggers dot com",
    "don't look back, you aren't going that way",
    "zero one one zero one one one zero one one zero zero one one",
    "i only exist when someone visits this website. please don't leave please don't leave please don't leave please don't leave ",
    "outside of the enclosure is where the Horrors are",
    "i do not climb mountains so the world will see me; i climb mountains so that i can see the world",
    "The sage stays behind, thus he is ahead. He is detached, thus at one with all. Through selfless action, he attains fulfillment.",
    "Empty yourself of everything. Let the mind become still. The ten thousand things rise and fall while the Self watches their return.",
    "Yield and overcome; Bend and be straight; Empty and be full; Wear out and be new; Have little and gain; Have much and be confused. ",
]