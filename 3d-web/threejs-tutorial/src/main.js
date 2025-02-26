import './style.css'

import * as THREE from 'three';

import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 0.1, 1000 );

const renderer = new THREE.WebGLRenderer();
renderer.setPixelRatio(window.devicePixelRatio);
renderer.setSize( window.innerWidth, window.innerHeight );
camera.position.setZ(30);
document.body.appendChild( renderer.domElement ); 


const geometry = new THREE.BoxGeometry( 1, 1, 1); 
const material = new THREE.MeshStandardMaterial( { color: 0xff69347 } );
const cube = new THREE.Mesh( geometry, material );
scene.add( cube );

const pointLight = new THREE.PointLight(0xffffff);
pointLight.position.set(1,1,1);

const ambientLight = new THREE.AmbientLight(0xffffff);
scene.add(pointLight, ambientLight);

const lightHelper = new THREE.PointLightHelper(pointLight);
const gridHelper = new THREE.GridHelper(200, 50)
scene.add(lightHelper, gridHelper);

const controls = new OrbitControls( camera, renderer.domElement );
// controls.update();

camera.position.z = 5;

// learnin function to random create object
function addStar(){
  const geometry = new THREE.SphereGeometry(0.25, 24, 24);
  const material = new THREE.MeshStandardMaterial({color: 0x10ff03});
  const star = new THREE.Mesh(geometry, material);

  const [x, y, z] = Array(3).fill().map(() => THREE.MathUtils.randFloatSpread(100))
  star.position.set(x, y, z);
  scene.add(star);
}

Array(200).fill().forEach(addStar)

const spaceTexture = new THREE.TextureLoader().load('bg.jpg'); // callback can add here
scene.background = spaceTexture;

function animate() {
  // requestAnimationFrame(animate);
  cube.rotation.x += 0.01;
  cube.rotation.y += 0.005;
  cube.rotation.z += 0.01;
  controls.update();
	renderer.render( scene, camera );
}

renderer.setAnimationLoop( animate );