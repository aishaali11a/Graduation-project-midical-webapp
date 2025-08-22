Medical Diagnosis Web Application

This repository contains the implementation of our web-based system  
developed as part of our graduation project.  
The system integrates machine learning predictions with a web platform  
to help doctors and patients manage medical data efficiently.

Project Overview
The platform allows patients and doctors to interact through a single system:  

- Patients can:
  - Create an account and log in.
  - Enter their vital signs manually or upload them automatically via sensors.
  - Receive feedback and recommendations from their doctor.

- Doctors can:
  - View their patients' medical data and vital signs.
  - See the system's predicted diagnosis based on the trained SVM model.
  - Make the final decision and send personalized notes or instructions back to the patient.

- System Intelligence:
  - The platform uses the trained SVM model to predict possible diseases based on patient data.
  - Doctors always have the final decision.

Features
- Secure patient login and registration.
- Real-time vital signs entry (manual or via sensors).
- Machine learning integration for disease prediction.
- Doctor dashboard for reviewing patient data.
- Ability to send notes and recommendations back to patients.


Contents
- /webapp → Frontend and backend implementation.
- /database → SQL scripts and database schema.
- /model → Final trained SVM model and prediction code.

Arduino Integration :

Some patient vital signs can be collected automatically using an Arduino-based sensor system
The Arduino captures the patient's vital parameters and can send the data to the web application  
for real-time monitoring and prediction.  

This integration for enhanced accuracy.
