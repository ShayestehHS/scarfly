
import {Routes, Route} from 'react-router-dom'
import Home from './components/PaymentResult/PaymentResult';




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
