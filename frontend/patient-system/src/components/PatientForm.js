import React, { useState } from 'react';
import ResponseModal from './ResultModal'; 

const PatientForm = () => {
  const [name, setName] = useState('');
  const [age, setAge] = useState('');
  const [sex, setSex] = useState('');
  const [eyeImage, setEyeImage] = useState(null);

  const [modalIsOpen, setModalIsOpen] = useState(false);
  const [responseMessage, setResponseMessage] = useState('');

  const [eyeImagePreviewUrl, setEyeImagePreviewUrl] = useState(null);

  const handleModalClose = () => {
    setModalIsOpen(false);
  };

  const handleNameChange = (e) => {
    setName(e.target.value);
  };

  const handleSexChange = (e) => {
    setSex(e.target.value);
  };

  const handleAgeChange = (e) => {
    setAge(e.target.value);
  };

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    setEyeImage(file);

    setEyeImagePreviewUrl(URL.createObjectURL(file)); // display the image preview

  };

  const handleSubmit = async (e) => {
    e.preventDefault();
  
    // Create a FormData object to handle file uploads
    const formData = new FormData();
    formData.append('name', name);
    formData.append('age', age);
    formData.append('sex', sex);
    formData.append('file', eyeImage);
  
    try {
      const response = await fetch('http://127.0.0.1:8000/predict', {
        method: 'POST',
        body: formData,
      });
  
      if (response.ok) {
        console.log('Patient data submitted successfully!');
        const data = await response.json();
        setResponseMessage(`
          Patient Name: ${data.patient.name}
          Patient Age: ${data.patient.age}
          Patient Sex: ${data.patient.sex}
          Prediction: ${data.prediction.class} 
        `);
        setModalIsOpen(true); // Open the modal
      } else {
        console.error('Error submitting patient data:', response.statusText);
        // Handle error cases
      }
    } catch (error) {
      console.error('An error occurred while submitting patient data:', error);
      // Handle network errors
    }
  };
  

  return (
    <div className="patient-form">
      <h2>Patient Information</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Name"
          value={name}
          onChange={handleNameChange} 
          required={true}
        />
        <input
          type="number"
          placeholder="Age"
          value={age}
          onChange={handleAgeChange}
          required={true}
        />
        <input
          type="text"
          placeholder="Sex"
          value={sex}
          onChange={handleSexChange}
          required={true}
        />
        <input
          type="file"
          accept="image/*"
          onChange={handleImageChange}
          required={true}
        />
        <button type="submit">Submit</button>
      </form>
      {eyeImagePreviewUrl && <img src={eyeImagePreviewUrl} alt="Eye Preview" className='preview-image' />}
      <ResponseModal
        isOpen={modalIsOpen}
        onRequestClose={handleModalClose}
        responseMessage={responseMessage}
        responseImage={eyeImagePreviewUrl}
      />
    </div>
  );
};

export default PatientForm;

