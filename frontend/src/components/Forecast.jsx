import React from 'react';

const Forecast = ({ data }) => {
    if (!data || !data.forecast_days) return null;

    const formatDay = (dateString) => {
        const options = { weekday: 'long' };
        return new Date(dateString).toLocaleDateString(undefined, options);
    };

    return (
        <section className="card">
            <header className="forecast-header">
                <h3>6-Day Forecast</h3>
                <span>Upcoming</span>
            </header>

            <div className="forecast-list">
                {data.forecast_days.map((day, index) => (
                    <article key={index} className="forecast-item">
                        <div className="forecast-icon">
                            {day.weather_description.toLowerCase().includes('rain') ? '🌧️' :
                                day.weather_description.toLowerCase().includes('cloud') ? '☁️' : '☀️'}
                        </div>
                        <div>
                            <div className="forecast-day">{formatDay(day.date)}</div>
                            <div className="forecast-desc">{day.weather_description}</div>
                        </div>
                        <div className="forecast-temps">
                            <div>{day.temperature_max}°</div>
                            <small>Low {day.temperature_min}°</small>
                        </div>
                    </article>
                ))}
            </div>
        </section>
    );
};

export default Forecast;
