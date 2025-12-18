/**
 * WeatherNow - Premium Weather Application
 * Created by: Soham
 * Copyright © 2025 Soham. All rights reserved.
 */

import { useState } from 'react'
import axios from 'axios'
import WeatherCard from './components/WeatherCard'
import Forecast from './components/Forecast'
import WeatherBackground from './components/WeatherBackground'
import Footer from './components/Footer'

function App() {
    const [city, setCity] = useState('')
    const [weather, setWeather] = useState(null)
    const [forecast, setForecast] = useState(null)
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)

    const fetchWeather = async (e) => {
        e.preventDefault()
        if (!city.trim()) return

        setLoading(true)
        setError(null)
        setWeather(null)
        setForecast(null)

        try {
            const [weatherRes, forecastRes] = await Promise.all([
                axios.get(`/api/weather?city=${city}`),
                axios.get(`/api/forecast?city=${city}`)
            ])
            setWeather(weatherRes.data)
            setForecast(forecastRes.data)
        } catch (err) {
            let message = 'Could not fetch weather data. Please try again.'
            if (err.response?.status === 404 && err.response?.data?.detail) {
                message = err.response.data.detail
            }
            setError(message)
            console.error('API Error:', err.response?.data || err.message)
            if (err.response) {
                console.error('Status:', err.response.status)
                console.error('Headers:', err.response.headers)
            }
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="app-wrapper">
            <WeatherBackground weather={weather} />

            <header className="app-header">
                <div className="logo">Weather<span>Now</span></div>
                <p className="subtitle">Animated weather and AQI dashboard.</p>
            </header>

            <div className="search-bar-wrapper">
                <form onSubmit={fetchWeather} className="search-bar">
                    <div className="search-input-wrapper">
                        <div className="search-icon">🔍</div>
                        <input
                            className="search-input"
                            type="text"
                            placeholder="Search city (try: Mumbai, London, Tokyo)"
                            value={city}
                            onChange={(e) => setCity(e.target.value)}
                        />
                    </div>
                    <button className="search-btn" type="submit" disabled={loading}>
                        {loading ? 'Loading...' : 'Search'}
                    </button>
                </form>
            </div>

            {error && (
                <div style={{ textAlign: 'center', color: '#ff4444', marginTop: '1rem' }}>
                    {error}
                </div>
            )}

            {(weather || forecast) && (
                <main className="cards-grid">
                    {/* Current Weather + AQI Section */}
                    {weather && <WeatherCard data={weather} />}

                    {/* Forecast Section */}
                    {forecast && <Forecast data={forecast} />}
                </main>
            )}

            {!loading && !error && !weather && !forecast && (
                <div style={{ textAlign: 'center', color: 'var(--text-muted)', marginTop: '2rem' }}>
                    Start by typing a city name above to see the current weather and 6-day forecast.
                </div>
            )}

            <Footer />
        </div>
    )
}

export default App
