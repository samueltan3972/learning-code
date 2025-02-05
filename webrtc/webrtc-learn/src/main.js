import './style.css'

// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import 'firebase/firestore'

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyCikcfL786AkxmBdvbFlOzX9RWoEHFoDE4",
  authDomain: "webrtc-learn-5e875.firebaseapp.com",
  projectId: "webrtc-learn-5e875",
  storageBucket: "webrtc-learn-5e875.firebasestorage.app",
  messagingSenderId: "164050647969",
  appId: "1:164050647969:web:b676bd1f8119bb1a45a9e0"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

const servers = {
  iceServers: [
    {
      urls: ["stun:stun.l.google.com:19302", "stun:stun.l.google.com:5349"],
    },
  ],
  iceCandidatePoolSize: 10,
}

// Global State
let pc = new RTCPeerConnection(servers);
let localStream = null;
let remoteStream = null;

// HTML elements
const webcamButton = document.getElementById('webcamButton');
const webcamVideo = document.getElementById('webcamVideo');
const callButton = document.getElementById('callButton');
const callInput = document.getElementById('callInput');
const answerButton = document.getElementById('answerButton');
const remoteVideo = document.getElementById('remoteVideo');
const hangupButton = document.getElementById('hangupButton');

// 1. Setup media sources
webcamButton.onclick = async () = > {
  localStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true});
  remoteStream = new MediaStream();

};