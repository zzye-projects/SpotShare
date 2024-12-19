import './ProgressBar.css';const ProgressBar = ({steps, currentStep}) => {
    if( steps < 2 ) { return null };

    return (
        <div className='progress-bar'>
            <div className='progress-step completed'/>
            {[...Array(steps - 1)].map((_, index) => (
                <div key={index} className='progress-fraction'>
                    <div className={`progress-connection ${index + 1 < currentStep? 'completed':''}`}/>
                    <div className={`progress-step ${index + 1 < currentStep? 'completed':''}`}/>
                </div>))}
        </div>
    )};

export default ProgressBar;