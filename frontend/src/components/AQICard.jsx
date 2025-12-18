import React from 'react';

const AQICard = ({ data }) => {
    if (!data) return null;

    const { aqi, pm2_5, pm10 } = data;

    // Determine label, class, and thumb position based on AQI
    let label = "Good";
    let colorClass = "aqi-good";
    let thumbPos = 10;

    if (aqi <= 50) {
        label = "Good";
        colorClass = "aqi-good";
        thumbPos = 12;
    } else if (aqi <= 100) {
        label = "Moderate";
        colorClass = "aqi-moderate";
        thumbPos = 30;
    } else if (aqi <= 150) {
        label = "Unhealthy for Sensitive Groups";
        colorClass = "aqi-unhealthy";
        thumbPos = 50;
    } else if (aqi <= 200) {
        label = "Unhealthy";
        colorClass = "aqi-unhealthy";
        thumbPos = 65;
    } else if (aqi <= 300) {
        label = "Very Unhealthy";
        colorClass = "aqi-unhealthy";
        thumbPos = 82;
    } else {
        label = "Hazardous";
        colorClass = "aqi-unhealthy";
        thumbPos = 94;
    }

    return (
        <article className={`aqi-card ${colorClass}`}>
            <div className="aqi-top">
                <div className="aqi-label">
                    <span className="aqi-live-dot"></span>
                    Live AQI
                </div>
                <div className="aqi-unit">(AQI-US)</div>
            </div>

            <div className="aqi-main-row">
                <div>
                    <div className="aqi-value">{aqi}</div>
                    <div style={{ fontSize: '11px', marginTop: '4px' }}>
                        PM2.5: <span>{pm2_5} μg/m³</span>
                    </div>
                    <div style={{ fontSize: '11px' }}>
                        PM10: <span>{pm10} μg/m³</span>
                    </div>
                </div>
                <div className="aqi-status-badge">{label}</div>
            </div>

            <div className="aqi-bars">
                <div className="aqi-scale">
                    <div className="aqi-thumb" style={{ left: `${thumbPos}%` }}></div>
                </div>
                <div className="aqi-bottom-labels">
                    <span>Good</span>
                    <span>Moderate</span>
                    <span>Poor</span>
                    <span>Unhealthy</span>
                    <span>Severe</span>
                    <span>Hazardous</span>
                </div>
            </div>
        </article>
    );
};

export default AQICard;
