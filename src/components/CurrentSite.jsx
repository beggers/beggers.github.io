import { FontLoader } from 'three/examples/jsm/loaders/FontLoader.js'
import { TextGeometry } from 'three/examples/jsm/geometries/TextGeometry.js'
import { extend, useThree } from '@react-three/fiber'
import { RotatingTorusKnot } from './RotatingTorusKnot'
import { Center, TrackballControls } from '@react-three/drei'

import font from '../../static/helvetiker_regular.typeface.json'

extend({ TextGeometry })

function CurrentSite() {
  const { camera, gl } = useThree()

  const bounds = 15
  const max_rot = 0.5

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

  let tori = []
  for (let i = 0; i < 30; i++) {
    tori.push(RotatingTorusKnot(pos(), rot(), rc(), false))
  }

  const fontLoader = new FontLoader().parse(font)

  return (
    <>
      <TrackballControls
        args={[camera, gl.domElement]}
        noPan={true}
        rotateSpeed={5.0}
      />
      <scene>
        {tori}
        <Center>
          <mesh center={true}>
            <textGeometry args={['Ben Eggers dot com', {
              font: fontLoader,
              size: 1.0,
              height: 0.2,
              curveSegments: 12,
              bevelEnabled: true,
              bevelThickness: 0.03,
              bevelSize: 0.02,
              bevelOffset: 0,
              bevelSegments: 5
            }]} />
            <meshNormalMaterial />
          </mesh>
        </Center>
      </scene>
    </>
  );
}

export { CurrentSite }
export default CurrentSite