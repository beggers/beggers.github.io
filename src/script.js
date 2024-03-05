// I'm using this to work through threejs-journey.com.
//
// TODO once I know more things -- do good software engineering (break
// this up into modules, etc.)

import './style.css'
import * as THREE from 'three'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js'
import { FontLoader } from 'three/examples/jsm/loaders/FontLoader.js'
import { TextGeometry } from 'three/examples/jsm/geometries/TextGeometry.js'

const canvas = document.querySelector('canvas.webgl')
const scene = new THREE.Scene()

const r = (min, max) => {
    return Math.random() * (max - min) + min
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

let bounds = 15;

const meshes = [];
for (let i = 0; i < geometries.length; i++) {
    const material = new THREE.MeshBasicMaterial({ color: rc(), wireframe: true })
    const mesh = new THREE.Mesh(geometries[i], material)
    meshes.push(mesh)
    mesh.position.x = r(-bounds, bounds)
    mesh.position.y = r(-bounds, bounds)
    mesh.position.z = r(-bounds, bounds)
    scene.add(mesh)
}

const max_rot = 0.001
const rotations = [];
for (let i = 0; i < geometries.length; i++) {
    rotations.push({
        x: r(-max_rot, max_rot),
        y: r(-max_rot, max_rot),
        z: r(-max_rot, max_rot)
    })
}

const fontLoader = new FontLoader()

fontLoader.load(
    '/helvetiker_regular.typeface.json',
    (font) => {
        const textGeometry = new TextGeometry(
            'Ben Eggers dot com',
            {
                font: font,
                size: 1.0,
                height: 0.2,
                curveSegments: 12,
                bevelEnabled: true,
                bevelThickness: 0.03,
                bevelSize: 0.02,
                bevelOffset: 0,
                bevelSegments: 5
            }
        )
        textGeometry.center()
        const textMaterial = new THREE.MeshNormalMaterial()
        const text = new THREE.Mesh(textGeometry, textMaterial)
        scene.add(text)
    }
)

const sizes = {
    width: window.innerWidth,
    height: window.innerHeight
}

window.addEventListener('resize', () => {
    sizes.width = window.innerWidth
    sizes.height = window.innerHeight

    camera.aspect = sizes.width / sizes.height
    camera.updateProjectionMatrix()

    renderer.setSize(sizes.width, sizes.height)
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
})

const camera = new THREE.PerspectiveCamera(75, sizes.width / sizes.height, 0.1, 100)
camera.position.z = bounds * 1.5
scene.add(camera)

const controls = new OrbitControls(camera, canvas)
controls.enableDamping = true

const renderer = new THREE.WebGLRenderer({
    canvas: canvas
})
renderer.setSize(sizes.width, sizes.height)
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))

const clock = new THREE.Clock()

const tick = () => {
    const elapsedTime = clock.getElapsedTime()
    for (let i = 0; i < meshes.length; i++) {
        meshes[i].rotation.x += rotations[i].x
        meshes[i].rotation.y += rotations[i].y
        meshes[i].rotation.z += rotations[i].z
    }
    controls.update()
    renderer.render(scene, camera)
    window.requestAnimationFrame(tick)
}

tick()