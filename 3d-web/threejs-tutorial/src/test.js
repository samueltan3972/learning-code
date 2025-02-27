import './style.css';
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { FirstPersonControls } from 'three/addons/controls/FirstPersonControls.js';

import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

// Create scene, camera, and renderer
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// Camera Position
camera.position.set(4, 2, 2);
camera.lookAt(0, 0, 0);

const loader = new GLTFLoader();

loader.load('/assets/car_model/source/car.glb', function (gltf) {
    const model = gltf.scene;
    model.scale.set(100, 100, 100); 
    model.position.set(0, 0, 0); // Move model to origin
    scene.add(model);
    console.log(scene.children); // See if the model is added to the scene

    animate()
}, undefined, function (error) {
    console.error('Error loading GLB model:', error);
});

// Lighting Setup
const pointLight = new THREE.PointLight(0xffffff);
pointLight.position.set(2, 2, 2);
pointLight.intensity = 5;

const ambientLight = new THREE.AmbientLight(0xffffff);
scene.add(pointLight, ambientLight);

// Helpers
const lightHelper = new THREE.PointLightHelper(pointLight);
const gridHelper = new THREE.GridHelper(200, 50);
scene.add(lightHelper, gridHelper);

const controls = new FirstPersonControls(camera, renderer.domElement);
controls.movementSpeed = 10;
controls.lookSpeed = 0.03;

// Background Texture
const spaceTexture = new THREE.TextureLoader().load('bg.jpg');
scene.background = spaceTexture;

const clock = new THREE.Clock();

// controls.addEventListener('change', () => {
//     camera.position.y = 10; // Lock Z position
// });

// Animation Loop
function animate() {
    const delta = clock.getDelta(); // Get time delta
    controls.update(delta); 

    camera.position.y = 2;
    renderer.render(scene, camera);
  }
  
renderer.setAnimationLoop(animate);
  