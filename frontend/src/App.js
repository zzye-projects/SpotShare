import './App.css';
import {Header, Main, Footer} from './components/layout';
import { BrowserRouter as Router } from 'react-router-dom';
import { AddressesProvider } from './context';

const App = () => {
  return (
  <Router>
    <Header/>
    <AddressesProvider>
      <Main/>
    </AddressesProvider>
    <Footer/>
  </Router>
)};

export default App;
