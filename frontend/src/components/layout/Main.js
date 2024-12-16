import './Main.css';
import { SearchForm } from '../forms';
import { FormPage } from '../pages';

const Main = () => (
    <section className='main'>
        <FormPage title='Find Parking'>
            <SearchForm/>
        </FormPage>
    </section>
);

export default Main;