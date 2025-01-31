## PDF to Speech Converter - Backend

### Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Backend Server](#running-the-backend-server)
- [Running Celery Worker](#running-celery-worker)
- [Database Migration](#database-migration)
- [Testing](#testing)
- [API Endpoints](#api-endpoints)
- [License](#license)

---

## Introduction

This directory contains the backend application for the **PDF to Speech Converter**. The backend is built using **Python Flask** and handles file uploads, text extraction, text cleaning, text-to-speech conversion, and provides API endpoints for the frontend to interact with.

---

## Prerequisites

- **Python 3.8+**
- **Redis**: For Celery message broker.
- **FFmpeg**: Required for audio processing.
- **Virtual Environment Tools**: `venv` or `conda`.

---

## Installation

### 1. Navigate to the Backend Directory

```bash
cd backend
```

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
```

### 3. Activate the Virtual Environment

- **On macOS/Linux:**

  ```bash
  source venv/bin/activate
  ```

- **On Windows:**

  ```bash
  venv\Scripts\activate
  ```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configuration

### 1. Environment Variables

Create a `.env` file in the `backend/` directory (optional) and set the following variables if needed:

```bash
# .env
FLASK_ENV=development
SECRET_KEY=your_secret_key
UPLOAD_FOLDER=uploads/pdfs
AUDIO_FOLDER=uploads/audios
LOG_DIR=logs
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
SQLALCHEMY_DATABASE_URI=sqlite:///tasks.db
```

### 2. Update `main.py` Configuration

Ensure that `app/main.py` reads the configuration from environment variables or uses default values.

---

## Running the Backend Server

From the `backend` directory, run:

```bash
python -m app.main
```

The backend server will start at `http://localhost:5000/`.

---

## Running Celery Worker

In a separate terminal window (with the virtual environment activated), run:

```bash
celery -A app.worker.celery worker --pool=threads --loglevel=INFO
```

This starts the Celery worker to process tasks asynchronously.

The `--pool=threads` flag is necessary as CUDA doesn't work with Celery's default prefork pooling.

---

## Database Migration

### 1. Initialize Migrations

```bash
flask db init
```

### 2. Generate Migration Script

```bash
flask db migrate -m "Initial migration"
```

### 3. Apply Migrations

```bash
flask db upgrade
```

---

## Testing

### Running Tests

Tests are located in the `app/tests/` directory. To run tests, execute:

```bash
pytest app/tests/
```

Ensure you have **pytest** installed:

```bash
pip install pytest
```

---

## API Endpoints

### 1. Upload PDF

- **Endpoint:** `/api/upload`
- **Method:** `POST`
- **Description:** Uploads a PDF file and initiates the conversion process.
- **Parameters:**
  - `file`: The PDF file to upload.
  - `voice`: The selected voice for TTS.

### 2. Check Task Status

- **Endpoint:** `/api/status/<task_id>`
- **Method:** `GET`
- **Description:** Retrieves the current status of the conversion task.

### 3. Download Audio

- **Endpoint:** `/api/download/<task_id>`
- **Method:** `GET`
- **Description:** Downloads the generated audio file.

### 4. Get Available Voices

- **Endpoint:** `/api/voices`
- **Method:** `GET`
- **Description:** Returns a list of available voice options.
