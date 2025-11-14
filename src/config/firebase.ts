import { initializeApp } from 'firebase/app';
import { getFirestore } from 'firebase/firestore';
import { getAuth } from 'firebase/auth';

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyBKp22uJ4hbb0-EbtQXMDdxQ114R_FopQ4",
  authDomain: "ap-dojo-6e565.firebaseapp.com",
  projectId: "ap-dojo-6e565",
  storageBucket: "ap-dojo-6e565.firebasestorage.app",
  messagingSenderId: "635100036283",
  appId: "1:635100036283:web:2a10e041b1bf025a557d9e",
  measurementId: "G-Z5479CZC3T"
};


// Firebaseを初期化
const app = initializeApp(firebaseConfig);

// Firestoreデータベースを取得
export const db = getFirestore(app);

// Firebase Authenticationを取得
export const auth = getAuth(app);

export default app;