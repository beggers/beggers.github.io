import * as THREE from 'three'
import * as Tone from 'tone'
import { FontLoader } from 'three/examples/jsm/loaders/FontLoader.js'
import { TextGeometry } from 'three/examples/jsm/geometries/TextGeometry.js'

import { useThree } from '@react-three/fiber'
import { RotatingWireframe } from './components/RotatingWireframe'

import { TrackballControls } from '@react-three/drei'

// import * as ac from './audio/ambientchords'
// const a = new ac.AmbientChords()
// let started = false
// addEventListener('mousemove', () => {
//   if (!started) {
//     Tone.start()
//     a.play()
//     started = true
//   }
// })

// const fontLoader = new FontLoader()

// fontLoader.load(
//   '/helvetiker_regular.typeface.json',
//   (font) => {
//     const textGeometry = new TextGeometry(
//       'Ben Eggers dot com',
//       {
//         font: font,
//         size: 1.0,
//         height: 0.2,
//         curveSegments: 12,
//         bevelEnabled: true,
//         bevelThickness: 0.03,
//         bevelSize: 0.02,
//         bevelOffset: 0,
//         bevelSegments: 5
//       }
//     )
//     textGeometry.center()
//     const textMaterial = new THREE.MeshNormalMaterial()
//     const text = new THREE.Mesh(textGeometry, textMaterial)
//     scene.add(text)
//   }
// )


function App() {
  const { camera, gl } = useThree()

  const bounds = 10
  const max_rot = 0.3

  const r = (min, max) => {
    return Math.random() * (max - min) + min
  }
  const pos = () => {
    return [r(-bounds, bounds), r(-bounds, bounds), r(-bounds, bounds)]
  }
  const rot = () => {
    return [r(-max_rot, max_rot), r(-max_rot, max_rot), r(-max_rot, max_rot)]
  }

  const rc = () => {
    const colors = [0xff0000, 0x00ff00, 0x0000ff]
    return colors[Math.floor(Math.random() * colors.length)]
  }

  const geometries = [
    new THREE.BoxGeometry(1, 1, 1),
    new THREE.CapsuleGeometry(1, 1, 4, 8),
    new THREE.CircleGeometry(1, 32),
    new THREE.ConeGeometry(1, 1, 32),
    new THREE.CylinderGeometry(1, 1, 1, 32),
    new THREE.DodecahedronGeometry(1, 10),
    new THREE.IcosahedronGeometry(1, 10),
    new THREE.OctahedronGeometry(1, 10),
    new THREE.PlaneGeometry(1, 1, 10, 10),
    new THREE.RingGeometry(1, 5, 32),
    new THREE.SphereGeometry(1, 32, 32),
    new THREE.TetrahedronGeometry(1, 10),
    new THREE.TorusGeometry(1, 0.3, 16, 100),
    new THREE.TorusKnotGeometry(1, 0.3, 128, 8),
  ]

  return (
    <>
      <TrackballControls
        args={[camera, gl.domElement]}
        noPan={true}
        noZoom={true}
        rotateSpeed={3.0}
      />
      <scene>
        {geometries.map((geometry) => {
          return (
            <RotatingWireframe
              geometry={geometry}
              pos={pos()}
              rot={rot()}
              color={rc()}
            />
          )
        })}
      </scene>
    </>
  );
}

export default App;
