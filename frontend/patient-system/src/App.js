import React from 'react';
import './App.css'; // Import your CSS file
import PatientForm from './components/PatientForm';
import About from './components/About';
import Footer from './components/Footer';

function App() {
  return (
    <div className="App">
      <h1>Eye Clinic Patient System</h1>
      <About/>
      <PatientForm />
      <Footer/>
    </div>
  );
}

export default App;

