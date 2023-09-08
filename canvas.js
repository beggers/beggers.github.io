// A rudimentary ascii canvas.

import { wrapInSpans } from "./utils.js";

export class Canvas {
    constructor(height, width) {
        this.height = height;
        this.width = width;
        this.canvas = Array(height);
        for (var i = 0; i < this.canvas.length; i++) {
            this.canvas[i] = Array(width).fill(" ");
        }
    }

    copyInAtPosition(item, y, x, c) {
        for (var i = 0; i < item.length; i++) {
            for (var j = 0; j < item[i].length; j++) {
                if (item[i][j] !== " " && item[i][j] !== "ñ") {
                    this.canvas[y + i][x + j] = wrapInSpans(item[i][j], c);
                }
            }
        }
    }

    getDisplayable() {
        var out = "";
        // We technically add 2 characters to the width. But who cares.
        const topAndBottom = wrapInSpans("+" + '-'.repeat(this.width) + "+\n", "fence");
        for (var i = 0; i < this.canvas.length; i++) {
            if (i === 0 || i === this.canvas.length - 1) {
                out += topAndBottom
            } else {
                out += wrapInSpans("|", "fence") + this.canvas[i].join('') + wrapInSpans("|", "fence") + "\n";
            }
        }
        return out;
    }
}