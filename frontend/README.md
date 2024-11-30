## PDF to Speech Converter - Frontend

### Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Frontend Server](#running-the-frontend-server)
- [Building for Production](#building-for-production)
- [Available Scripts](#available-scripts)
- [Project Structure](#project-structure)
- [License](#license)

---

## Introduction

This directory contains the frontend application for the **PDF to Speech Converter**. The frontend is built using **React** and provides a user interface for uploading PDFs, selecting voices, and playing or downloading the generated audio.

---

## Prerequisites

- **Node.js 14+**
- **npm** (comes with Node.js)

---

## Installation

### 1. Navigate to the Frontend Directory

```bash
cd frontend
```

### 2. Install Dependencies

```bash
npm install
```

---

## Configuration

### 1. Environment Variables

Create a `.env` file in the `frontend/` directory to set environment-specific variables:

```bash
# .env
REACT_APP_API_BASE_URL=http://localhost:5000/api
```

### 2. Update API Base URL (if necessary)

Ensure that the `API_BASE_URL` in `src/services/api.js` points to your backend API endpoint.

---

## Running the Frontend Server

```bash
npm start
```

The application will be available at `http://localhost:3000/`.

---

## Building for Production

To build the app for production, run:

```bash
npm run build
```

This will create an optimized build in the `build/` directory.

---

## Available Scripts

In the project directory, you can run:

- **`npm start`**: Runs the app in development mode.
- **`npm run build`**: Builds the app for production.
- **`npm test`**: Launches the test runner.
- **`npm run eject`**: Ejects the app from Create React App configuration (this action is irreversible).

---

## Project Structure

```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── index.js
│   ├── App.js
│   ├── components/
│   │   ├── Header.js
│   │   ├── UploadForm.js
│   │   ├── VoiceSelector.js
│   │   └── AudioPlayer.js
│   ├── services/
│   │   └── api.js
│   ├── styles/
│   │   └── App.css
│   └── assets/
├── package.json
├── package-lock.json
└── README.md
```

- **public/**: Contains the HTML template.
- **src/**: Contains the React components and source code.
  - **components/**: Reusable React components.
  - **services/**: API service modules.
  - **styles/**: CSS stylesheets.
  - **assets/**: Static assets like images and fonts.
- **package.json**: Project metadata and dependencies.
- **README.md**: Documentation for the frontend application.

