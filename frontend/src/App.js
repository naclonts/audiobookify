// frontend/src/App.js

import React from 'react';
import Header from './components/Header';
import UploadForm from './components/UploadForm';

function App() {
  return (
    <div className="App">
      <Header />
      <main>
        <UploadForm />
      </main>
    </div>
  );
}

export default App;
