import React from 'react';

const About = () => {
    return (
        <div className="container center">
            <div className="about">
                <div className="about__content">
                    <h2 className="about__title" style={{paddingTop: 20}}>About Strabismus Detector</h2>
                    <p className="about__description" style={{textAlign: "justify", padding:40}}>
                        Strabismus Detector is an advanced AI-powered tool designed to detect various types of
                        strabismus, also known as eye misalignment. Our cutting-edge technology can identify four
                        primary types of strabismus, including:<br></br>
                        <span className="list_strabismus">
                        Esotropia,
                        Exotropia,
                        Hypertropia, and
                        Hypotropia.
                        </span>
                        <br></br>
                        With high accuracy and precision, our tool assists healthcare professionals in diagnosing and
                        managing strabismus conditions effectively. Early detection and intervention are crucial in
                        preventing vision impairment and improving the quality of life for individuals affected by
                        strabismus. Strabismus Detector aims to streamline the diagnostic process, providing timely
                        insights to healthcare providers and enhancing patient care.
                    </p>
                </div>
            </div>
        </div>
    );
};

export default About;