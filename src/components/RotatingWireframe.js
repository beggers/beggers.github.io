import { useFrame } from '@react-three/fiber'
import { useRef } from 'react'

function RotatingWireframe(geometry, pos, rot, color) {
  // console.log(geometry, pos, rot, color)
  // const meshRef = useRef()
  // console.log(meshRef.current)
  // useFrame((state, delta) => {
  //   meshRef.current.rotation.x += rot[0] * delta
  //   meshRef.current.rotation.y += rot[1] * delta
  //   meshRef.current.rotation.z += rot[2] * delta
  // })
  return (
    <mesh position={pos} rotation={rot} key={pos}>
      <torusKnotGeometry args={[1, 0.3, 128, 8]} />
      <meshBasicMaterial color={color} wireframe={true} />
    </mesh>
  )
}

export { RotatingWireframe }
export default RotatingWireframe;
