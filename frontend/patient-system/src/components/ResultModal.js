import React from 'react';
import Modal from 'react-modal';

// Define the custom styles
const customStyles = {
  content: {
    background: '#1a1a1a',
    color: '#ffffff',
    border: 'none',
    borderRadius: '10px',
    maxWidth: '800px',
    margin: 'auto',
    fontFamily: 'sans-serif', // Use sans-serif font
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
  },
};

const ResponseModal = ({ isOpen, onRequestClose, responseMessage, responseImage }) => {
  return (
    <Modal
      isOpen={isOpen}
      onRequestClose={onRequestClose}
      contentLabel="Response Modal"
      style={customStyles} // Apply the custom styles
    >
      <h2>Prediction Result</h2>
      <div>
        {responseMessage.split('\n').map((line, index) => (
          <p key={index}>{line}</p>
        ))}
        {responseImage && <img src={responseImage} alt="Prediction Result" className='preview-image' />}
      </div>
      <button
        onClick={onRequestClose}
        style={{
          position: 'absolute',
          top: '10px',
          right: '10px',
          background: 'none',
          border: 'none',
          color: 'white',
          cursor: 'pointer',
          fontSize: '20px', // Make the close button a cross
        }}
      >
        &times; {/* Use the HTML entity for a cross */}
      </button>
    </Modal>
  );
};

export default ResponseModal;
