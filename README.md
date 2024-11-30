
🏗️ This is a work in progress and not fully functioning yet! 🏗️

---

# Audiobookify

## PDF to Speech Converter

### Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation and Setup](#installation-and-setup)
- [Running the Application](#running-the-application)
- [License](#license)

---

## Introduction

The **PDF to Speech Converter** is a web application that allows users to upload PDF documents and receive high-quality spoken audio as output. Users can choose from multiple voice options, ensuring a personalized listening experience. The application processes the PDF by extracting and cleaning the text before converting it to speech using advanced text-to-speech (TTS) models.

---

## Features

- **PDF Upload**: Upload PDF files directly through the web interface.
- **Voice Selection**: Choose from a variety of high-quality voices.
- **Text Cleaning**: Automatic removal of headers, footers, and hyphenations for smooth narration.
- **Audio Playback and Download**: Listen to the generated audio online or download it for offline use.
- **Asynchronous Processing**: Efficient handling of large files without blocking the user interface.
- **Modular Design**: Separate backend and frontend components for scalability and maintainability.

---

## Project Structure

```
project-root/
├── backend/
│   ├── app/
│   ├── requirements.txt
│   └── run.py
├── frontend/
│   ├── public/
│   ├── src/
│   ├── package.json
│   └── README.md
├── docker/
│   ├── Dockerfile.backend
│   ├── Dockerfile.frontend
│   └── docker-compose.yml
├── scripts/
│   └── setup_env.sh
├── .gitignore
└── README.md
```

- **backend/**: Contains the Python Flask backend application.
- **frontend/**: Contains the React frontend application.
- **docker/**: Docker configuration files for containerization.
- **scripts/**: Scripts for environment setup and maintenance.
- **.gitignore**: Specifies files for Git to ignore.
- **README.md**: Documentation for the overall application.

---

## Prerequisites

- **Python 3.8+**
- **Node.js 14+ and npm**
- **Redis**: For Celery message broker.
- **FFmpeg**: For audio processing (required by some TTS models).
- **Git**: Version control system.
- **Virtual Environment Tools**: `venv` or `conda` for Python.

---

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/pdf-to-speech-converter.git
cd pdf-to-speech-converter
```

### 2. Backend Setup

Follow the instructions in the [backend README](backend/README.md) to set up the backend environment.

### 3. Frontend Setup

Follow the instructions in the [frontend README](frontend/README.md) to set up the frontend environment.

### 4. Configure Environment Variables

Create `.env` files in both the `backend/` and `frontend/` directories if needed, and set the necessary environment variables as specified in their respective README files.

---

## Running the Application

### 1. Start the Backend Server

Navigate to the `backend/` directory and run:

```bash
cd backend
python run.py
```

Ensure that the backend server is running at `http://localhost:5000/`.

### 2. Start the Celery Worker

In a separate terminal, navigate to the `backend/` directory and run:

```bash
cd backend
celery -A app.controllers.tasks.celery worker --loglevel=info
```

This starts the Celery worker to process tasks asynchronously.

### 3. Start the Frontend Server

Navigate to the `frontend/` directory and run:

```bash
cd frontend
npm start
```

The frontend application will be available at `http://localhost:3000/`.


