import './ProgressBar.css';const ProgressBar = ({totalSteps, currentStep}) => {
    if( totalSteps < 2 ) { return null };
    return (
        <div className='progress-bar'>
            <div className='progress-step completed'/>
            {[...Array(totalSteps - 1)].map((_, index) => (
                <div key={index} className='progress-fraction'>
                    <div className={`progress-connection ${index + 1 < currentStep? 'completed':''}`}/>
                    <div className={`progress-step ${index + 1 < currentStep? 'completed':''}`}/>
                </div>))}
        </div>
    )};

export default ProgressBar;