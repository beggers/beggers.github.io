// A rudimentary ascii canvas.

import { wrapInSpans } from "./utils.js";

export class Canvas {
    constructor(height, width) {
        this.height = height;
        this.width = width;
        this.canvas = Array(height);
        for (var i = 0; i < this.canvas.length; i++) {
            this.canvas[i] = Array(width).fill(".");
        }
    }

    copyInAtPosition(item, y, x, c) {
        for (var i = 0; i < item.length; i++) {
            for (var j = 0; j < item[i].length; j++) {
                if (item[i][j] !== " ") {
                    this.canvas[y + i][x + j] = wrapInSpans(item[i][j], c);
                }
            }
        }
    }

    getDisplayable() {
        var out = "";
        for (var i = 0; i < this.canvas.length; i++) {
            out += `${i}\t` + this.canvas[i].join('') + "\n";
        }
        return out;
    }
}