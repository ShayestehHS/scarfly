import {Routes, Route} from 'react-router-dom'
import Home from './components/PaymentResult/PaymentResult';


if (window.location.origin === "http://localhost:3000") {
  axios.defaults.baseURL = "http://127.0.0.1:8000";
} else {
  axios.defaults.baseURL = window.location.origin;
}


import Product from './components/product/Product';

function App() {
  return (
    <Routes>
      <Route path='/orders/verify/' element={<Home/>} />
      <Route path='/products/:productID' element={<Product/>} />
    </Routes>
  );
}

export default App;
