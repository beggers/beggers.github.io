import * as Tone from 'tone'

import { Chord, Interval, Note, Scale } from "tonal";
import { DefaultChordExplorer } from "./music/chordexplorer";

// TODO find a better way to do this. Probably need a button to be clicked
// on load?
addEventListener('mousemove', () => {
  Tone.start()
})

export default class AmbientAudio {
  constructor() {
    // TODO spend some time designing the pad for this on the OP-1 and
    // replace this awful synth.
    this.synth = new Tone.PolySynth().toDestination()
    this.chordExplorer = new DefaultChordExplorer()
    this.currentChord = this.chordExplorer.startingChord()
    this.nextChord = this.chordExplorer.nextChord(this.currentChord)
    // TODO tweak
    this.duration = 7.5
  }

  play() {
    // TODO find a way to get info into or out of this function so lights can
    // respond to music.

    let updateAndPlayOnce = this.updateAndPlayOnce.bind(this)
    updateAndPlayOnce()
    var intervalId = window.setInterval(function () {
      updateAndPlayOnce()
    }, 8000);
  }

  updateAndPlayOnce() {
    this.currentChord = this.nextChord
    this.nextChord = this.chordExplorer.nextChord(this.currentChord)
    let now = Tone.now()
    this.synth.triggerAttack(this.currentChord, now);
    this.synth.triggerRelease(this.currentChord, now + this.duration);
  }
}
