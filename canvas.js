// A rudimentary ascii canvas.

export class Canvas {
    constructor(height, width) {
        this.height = height;
        this.width = width;
        this.canvas = Array(height);
        for (var i = 0; i < this.canvas.length; i++) {
            this.canvas[i] = Array(width).fill(".");
        }
    }

    copyInAtPosition(item, y, x) {
        for (var i = 0; i < item.length; i++) {
            for (var j = 0; j < item[i].length; j++) {
                this.canvas[y + i][x + j] = item[i][j];
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