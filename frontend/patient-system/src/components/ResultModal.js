// ResponseModal.js
import React from 'react';
import Modal from 'react-modal';

const customStyles = {
  content: {
    background: '#1a1a1a', 
    color: '#ffffff !important', 
    border: 'none',
    borderRadius: '10px',
    maxWidth: '400px', // Adjust as needed
    margin: 'auto',
  },
};


const ResponseModal = ({ isOpen, onRequestClose, responseMessage }) => {
  return (
    <Modal
      isOpen={isOpen}
      onRequestClose={onRequestClose}
      contentLabel="Response Modal"
      customStyles={customStyles}
    >
      <h2>Prediction Result</h2>
      <div>
        {responseMessage.split('\n').map((line, index) => (
          <p key={index}>{line}</p>
        ))}
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
        }}
      > Close </button>
    </Modal>
  );
};

export default ResponseModal;
