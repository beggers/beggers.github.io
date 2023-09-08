export const getSaying = function() {
    return sayings[sayings.length * Math.random() | 0]
}

// The sayings themselves. If the list has two items, it's a dialogue and needs
// two animals.
export const sayings = [
    [
        "ben eggers dot gov"
    ],
    [
        "don't look back, you aren't going that way",
    ],
    [
        "zero one one zero one one one zero one one zero zero one one"
    ],
    [
        "i only exist when someone visits this website. please don't leave please don't leave please don't leave please don't leave "
    ],
    [
        "outside of my enclosure is where the Horrors are"
    ],
    [
        "i do not climb mountains so the world will see me; i climb mountains so that i can see the world"
    ]
]