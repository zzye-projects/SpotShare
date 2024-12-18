import './App.css';
import {Header, Main, Footer} from './components/layout';
import { BrowserRouter as Router } from 'react-router-dom';

const App = () => {
  return (
  <Router>
    <Header/>
    <Main/>
    <Footer/>
  </Router>
)};

export default App;
