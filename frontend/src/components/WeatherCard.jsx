import React from 'react';

const WeatherCard = ({ data }) => {
    if (!data) return null;

    const {
        city,
        country,
        temperature,
        feels_like,
        humidity,
        wind_speed,
        pressure,
        weather_description,
        visibility,
        timestamp,
        air_quality
    } = data;

    const formatDate = (dateString) => {
        const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
        return new Date(dateString).toLocaleDateString(undefined, options);
    };

    const formatTime = (dateString) => {
        return new Date(dateString).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    };

    return (
        <section className="card">
            <div className="location-header">
                <div className="location-meta">
                    <div style={{ display: 'flex', alignItems: 'center', flexWrap: 'wrap' }}>
                        <h2>{city}</h2>
                        <span className="chip-pill">{country}</span>
                    </div>
                    <p>Current Weather</p>
                    <div className="date-text">
                        {formatDate(timestamp)} • {formatTime(timestamp)}
                    </div>
                </div>

                <div className="weather-icon-wrapper">
                    <div className="sun-core">
                        <div className="sun-ray"></div>
                    </div>
                </div>
            </div>

            <div className="temp-main-row">
                <div>
                    <div className="temp-main">
                        {temperature}°<small>C</small>
                    </div>
                    <div className="temp-desc">
                        <span>{weather_description}</span> • Feels like {feels_like}°
                    </div>
                </div>

                <div className="badge">
                    <span className="badge-dot"></span>
                    Live • Updated just now
                </div>
            </div>

            <div className="current-bottom-grid">
                <div className="metric-grid">
                    <article className="metric-card">
                        <div className="metric-icon">🍃</div>
                        <div className="metric-label">Wind</div>
                        <div className="metric-value">{wind_speed} km/h</div>
                        <div className="metric-sub">Light breeze</div>
                    </article>

                    <article className="metric-card">
                        <div className="metric-icon">💧</div>
                        <div className="metric-label">Humidity</div>
                        <div className="metric-value">{humidity}%</div>
                        <div className="metric-sub">Atmosphere</div>
                    </article>

                    <article className="metric-card">
                        <div className="metric-icon">🌡️</div>
                        <div className="metric-label">Pressure</div>
                        <div className="metric-value">{pressure} hPa</div>
                        <div className="metric-sub">Stable</div>
                    </article>

                    <article className="metric-card">
                        <div className="metric-icon">👀</div>
                        <div className="metric-label">Visibility</div>
                        <div className="metric-value">{visibility ? `${visibility} km` : 'N/A'}</div>
                        <div className="metric-sub">Clear views</div>
                    </article>
                </div>

                {air_quality && (
                    <div className="aqi-box">
                        <h3>Live AQI</h3>
                        <span>{air_quality.aqi}</span>
                        <div style={{ fontSize: '12px', marginTop: '4px' }}>
                            Status: <strong>{air_quality.category}</strong>
                        </div>
                    </div>
                )}
            </div>
        </section>
    );
};

export default WeatherCard;
