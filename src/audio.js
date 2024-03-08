import * as Tone from 'tone'

import { Chord, Interval, Note, Scale } from "tonal";

// TODO find a better way to do this. Probably need a button to be clicked
// on load?
// addEventListener('mousemove', () => {
//   Tone.start()
// })

export default class AmbientAudio {
  constructor() {
    // TODO spend some time designing the pad for this on the OP-1 and
    // replace this awful synth.
    this.synth = new Tone.PolySynth().toDestination()
    this.currentChord = Chord.notes("m6", "C4")
    this.nextChord = this.findNextChord()
    // TODO tweak
    this.duration = 1.5
  }

  findNextChord() {
    // TODO in addition to fixing the random note logic, we could probably
    // vaccilate between complexity and simplicity, maybe even tension
    // and resolution.

    let newChord = this.currentChord.slice()
    newChord.splice(Math.floor(Math.random() * newChord.length), 1)
    // TODO this needs to be aware of chord shapes and choose notes that
    // make sense. Sounds terrible rn.
    newChord.push(Note.fromMidi(Math.floor(Math.random() * 12) + 60))
    return newChord
  }

  play() {
    // TODO find a way to get info into or out of this function so lights can
    // respond to music.

    let updateAndPlayOnce = this.updateAndPlayOnce.bind(this)
    updateAndPlayOnce()
    var intervalId = window.setInterval(function () {
      updateAndPlayOnce()
    }, 2000);
  }

  updateAndPlayOnce() {
    this.currentChord = this.nextChord
    this.nextChord = this.findNextChord()
    let now = Tone.now()
    this.synth.triggerAttack(this.currentChord, now);
    this.synth.triggerRelease(this.currentChord, now + this.duration);
  }
}
