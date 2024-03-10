import * as Tone from 'tone'

import { DefaultChordManager } from "./chordmanager";

class AmbientChords {
  constructor() {
    // TODO spend some time designing the pad for this on the OP-1 and
    // replace this awful synth.
    this.synth = new Tone.PolySynth().toDestination()
    this.synth.set({
      detune: 10,
      envelope: {
        attack: 30,
        release: 1,
        attackCurve: "linear",
        decayCurve: "exponential",
        releaseCurve: "exponential"
      }
    });
    this.chordExplorer = new DefaultChordManager()
    this.currentChord = this.chordExplorer.startingChord()
    this.nextChord = this.chordExplorer.nextChord(this.currentChord)
    // TODO tweak
    this.duration = 7.5
  }

  play() {
    // TODO find a way to get info into or out of this function so lights can
    // respond to music.

    let updateAndPlayOnce = this.updateAndPlayOnce.bind(this)
    this.playCurrentChord()
    var intervalId = window.setInterval(function () {
      updateAndPlayOnce()
    }, 8000);
  }

  playCurrentChord() {
    let now = Tone.now()
    let withBass = this.currentChord.withRandomBass(2)
    console.log(withBass)
    this.synth.triggerAttack(withBass, now);
    this.synth.triggerRelease(withBass, now + this.duration);
  }

  updateAndPlayOnce() {
    this.currentChord = this.nextChord
    this.nextChord = this.chordExplorer.nextChord(this.currentChord)
    this.playCurrentChord()
  }
}

export { AmbientChords }
export default AmbientChords