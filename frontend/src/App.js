import './App.css';
import {Header, Main, Footer} from './components/layout';

const App = () => {
  const footerItems = ['About Us', 'Terms of Use', 'Careers', 'Contact Us']
  return (
  <>
    <Header/>
    <Main/>
    <Footer items={footerItems}/>
  </>
)};

export default App;
