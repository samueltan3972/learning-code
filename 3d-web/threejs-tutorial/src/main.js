import './style.css';
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

// Scene Setup
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer();

renderer.setPixelRatio(window.devicePixelRatio);
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// Camera Position
camera.position.setZ(30);

// Torus Object
const torusGeometry = new THREE.TorusGeometry(4, 1, 3, 30);
const torusMaterial = new THREE.MeshStandardMaterial({ color: 0xff69347 });
const torusMesh = new THREE.Mesh(torusGeometry, torusMaterial);
scene.add(torusMesh);

// Lighting Setup
const pointLight = new THREE.PointLight(0xffffff);
pointLight.position.set(2, 2, 2);

const ambientLight = new THREE.AmbientLight(0xffffff);
scene.add(pointLight, ambientLight);

// Helpers
const lightHelper = new THREE.PointLightHelper(pointLight);
const gridHelper = new THREE.GridHelper(200, 50);
scene.add(lightHelper, gridHelper);

// Controls
const controls = new OrbitControls(camera, renderer.domElement);

// Function to Generate Random Stars
function createRandomStar() {
  const starGeometry = new THREE.SphereGeometry(0.25, 24, 24);
  const starMaterial = new THREE.MeshStandardMaterial({ color: 0x10ff03 });
  const starMesh = new THREE.Mesh(starGeometry, starMaterial);
  
  const [x, y, z] = Array(3).fill().map(() => THREE.MathUtils.randFloatSpread(100));
  starMesh.position.set(x, y, z);
  scene.add(starMesh);
}

Array(200).fill().forEach(createRandomStar);

// Background Texture
const spaceTexture = new THREE.TextureLoader().load('bg.jpg');
scene.background = spaceTexture;

// Textured Cube
const texture = new THREE.TextureLoader().load('tilling-texture.jpg');
const texturedCube = new THREE.Mesh(
  new THREE.BoxGeometry(3, 3, 3),
  new THREE.MeshBasicMaterial({ map: texture })
);
scene.add(texturedCube);

// Animation Loop
function animate() {
  torusMesh.rotation.x += 0.01;
  torusMesh.rotation.y += 0.005;
  torusMesh.rotation.z += 0.01;
  
  controls.update();
  renderer.render(scene, camera);
}

renderer.setAnimationLoop(animate);
