import { useFrame } from '@react-three/fiber'
import { useRef } from 'react'

const initialRot = () => {
  return [Math.random() * 180, Math.random() * 180, Math.random() * 180]
}

function RotatingTorusKnot({ pos, rot, color }) {
  const meshRef = useRef()
  useFrame((state, delta) => {
    meshRef.current.rotation.x += rot[0] * delta
    meshRef.current.rotation.y += rot[1] * delta
    meshRef.current.rotation.z += rot[2] * delta
  })
  return (
    <>
      <mesh ref={meshRef} position={pos} rotation={initialRot()} key={pos}>
        <torusKnotGeometry args={[0.8, 0.1, 128, 8]} />
        <meshBasicMaterial color={color} wireframe={true} />
      </mesh>
    </>
  )
}

export { RotatingTorusKnot }
export default RotatingTorusKnot;
