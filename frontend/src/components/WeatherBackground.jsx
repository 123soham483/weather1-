import React, { useEffect, useState } from 'react';

const WeatherBackground = ({ weather }) => {
    const [mode, setMode] = useState('default');

    useEffect(() => {
        if (!weather || !weather.weather_description) {
            setMode('default');
            return;
        }

        const desc = weather.weather_description.toLowerCase();

        if (desc.includes('rain') || desc.includes('drizzle') || desc.includes('thunder')) {
            setMode('rainy');
        } else if (desc.includes('snow') || desc.includes('sleet') || desc.includes('blizzard')) {
            setMode('snowy');
        } else if (desc.includes('clear') || desc.includes('sun')) {
            setMode('sunny');
        } else if (desc.includes('cloud') || desc.includes('overcast')) {
            setMode('cloudy');
        } else {
            setMode('sunny');
        }
    }, [weather]);

    // Generate rain particles
    const rainParticles = Array.from({ length: 150 }, (_, i) => (
        <div
            key={`rain-${i}`}
            className="rain-particle"
            style={{
                left: `${Math.random() * 100}%`,
                animationDelay: `${Math.random() * 2}s`,
                animationDuration: `${0.5 + Math.random() * 0.5}s`
            }}
        />
    ));

    // Generate snow particles
    const snowParticles = Array.from({ length: 100 }, (_, i) => (
        <div
            key={`snow-${i}`}
            className="snow-particle"
            style={{
                left: `${Math.random() * 100}%`,
                animationDelay: `${Math.random() * 5}s`,
                animationDuration: `${3 + Math.random() * 2}s`,
                fontSize: `${10 + Math.random() * 10}px`
            }}
        >
            ❄
        </div>
    ));

    return (
        <div className={`weather-bg ${mode}`}>
            {/* Animated Sun for Sunny Weather */}
            {mode === 'sunny' && (
                <div className="sun-animated">
                    <div className="sun-core-big"></div>
                </div>
            )}

            {/* City Skyline */}
            <div className="city-skyline">
                <div className="building" style={{ height: '120px', left: '5%' }}></div>
                <div className="building" style={{ height: '180px', left: '10%' }}></div>
                <div className="building" style={{ height: '90px', left: '15%' }}></div>
                <div className="building" style={{ height: '160px', left: '20%' }}></div>
                <div className="building" style={{ height: '140px', left: '25%' }}></div>
                <div className="building" style={{ height: '100px', left: '30%' }}></div>
                <div className="building" style={{ height: '190px', left: '35%' }}></div>
                <div className="building" style={{ height: '130px', left: '40%' }}></div>
                <div className="building" style={{ height: '110px', left: '45%' }}></div>
                <div className="building" style={{ height: '170px', left: '50%' }}></div>
                <div className="building" style={{ height: '95px', left: '55%' }}></div>
                <div className="building" style={{ height: '150px', left: '60%' }}></div>
                <div className="building" style={{ height: '125px', left: '65%' }}></div>
                <div className="building" style={{ height: '185px', left: '70%' }}></div>
                <div className="building" style={{ height: '105px', left: '75%' }}></div>
                <div className="building" style={{ height: '145px', left: '80%' }}></div>
                <div className="building" style={{ height: '115px', left: '85%' }}></div>
                <div className="building" style={{ height: '165px', left: '90%' }}></div>
                <div className="building" style={{ height: '135px', left: '95%' }}></div>
            </div>

            {/* Clouds for cloudy/default weather */}
            {(mode === 'cloudy' || mode === 'default') && (
                <>
                    <div className="cloud cloud-1"></div>
                    <div className="cloud cloud-2"></div>
                    <div className="cloud cloud-3"></div>
                </>
            )}

            {/* Rain Effect */}
            {mode === 'rainy' && (
                <>
                    <div className="rain-container">{rainParticles}</div>
                    <div className="lightning-flash"></div>
                </>
            )}

            {/* Snow Effect */}
            {mode === 'snowy' && (
                <div className="snow-container">{snowParticles}</div>
            )}
        </div>
    );
};

export default WeatherBackground;
