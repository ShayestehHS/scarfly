import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import { BrowserRouter } from 'react-router-dom'
import { Toaster } from 'react-hot-toast';

ReactDOM.render(
  <React.StrictMode>
    <BrowserRouter>
 
    <Toaster
  position="top-center"
  reverseOrder={false}
/>
      <App />
    </BrowserRouter>
  </React.StrictMode>,
  document.getElementById('root')
);

