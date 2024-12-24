import './App.css';
import {Header, Main, Footer} from './components/layout';
import { BrowserRouter as Router } from 'react-router-dom';
import { AddressesProvider, VehiclesProvider } from './context';

const App = () => {

  return (
  <Router>
    <Header/>
    <AddressesProvider>
      <VehiclesProvider>
        <Main/>
      </VehiclesProvider>
    </AddressesProvider>
    <Footer/>
  </Router>
)};

export default App;
