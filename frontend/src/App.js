import './App.css';
import Header from './components/Header';
import Main from './components/Main';
import Footer from './components/Footer';

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
