import React, { useEffect, useMemo, useState } from 'react';
import { createRoot } from 'react-dom/client';
import './styles.css';

function App() {
    const [hotels, setHotels] = useState([]);
    const [city, setCity] = useState('');
    const [roomType, setRoomType] = useState('');
    const [checkIn, setCheckIn] = useState('');
    const [checkOut, setCheckOut] = useState('');
    const [guests, setGuests] = useState(1);

    const [result, setResult] = useState(null);
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        fetch('/api/hotels')
            .then(res => res.json())
            .then(data => setHotels(data))
            .catch(() => setError('No fue posible cargar las sedes.'));
    }, []);

    const cities = useMemo(() => {
        return [...new Set(hotels.map(item => item.city))];
    }, [hotels]);

    const roomTypes = useMemo(() => {
        return hotels
            .filter(item => item.city === city)
            .map(item => item.room_type);
    }, [hotels, city]);

    function handleCityChange(value) {
        setCity(value);
        setRoomType('');
        setResult(null);
    }

    async function search(event) {
        event.preventDefault();

        setError('');
        setResult(null);
        setLoading(true);

        try {
            const params = new URLSearchParams({
                city,
                room_type: roomType,
                check_in: checkIn,
                check_out: checkOut,
                guests: String(guests)
            });

            const response = await fetch(`/api/availability?${params}`);

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'Error consultando disponibilidad.');
            }

            setResult(data);

        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    }

    const money = value =>
        new Intl.NumberFormat('es-CO', {
            style: 'currency',
            currency: 'COP',
            maximumFractionDigits: 0
        }).format(value);

    return (
        <div className="app">

            <header className="hero">
                <div>
                    <span className="eyebrow">CADENA HOTELERA</span>
                    <h1>Encuentra tu próxima estadía</h1>
                    <p>
                        Consulta habitaciones disponibles y conoce el valor
                        estimado de tu alojamiento.
                    </p>
                </div>
            </header>

            <main className="container">

                <section className="search-card">
                    <div className="section-title">
                        <span>01</span>
                        <div>
                            <h2>Consultar disponibilidad</h2>
                            <p>Selecciona los datos de tu viaje.</p>
                        </div>
                    </div>

                    <form onSubmit={search} className="search-form">

                        <label>
                            <span>Sede</span>
                            <select
                                value={city}
                                onChange={e => handleCityChange(e.target.value)}
                                required
                            >
                                <option value="">Seleccionar ciudad</option>

                                {cities.map(item => (
                                    <option key={item} value={item}>
                                        {item}
                                    </option>
                                ))}
                            </select>
                        </label>

                        <label>
                            <span>Alojamiento</span>
                            <select
                                value={roomType}
                                onChange={e => setRoomType(e.target.value)}
                                required
                                disabled={!city}
                            >
                                <option value="">Seleccionar tipo</option>

                                {roomTypes.map(item => (
                                    <option key={item} value={item}>
                                        {item.charAt(0).toUpperCase() + item.slice(1)}
                                    </option>
                                ))}
                            </select>
                        </label>

                        <label>
                            <span>Fecha de entrada</span>
                            <input
                                type="date"
                                value={checkIn}
                                onChange={e => setCheckIn(e.target.value)}
                                required
                            />
                        </label>

                        <label>
                            <span>Fecha de salida</span>
                            <input
                                type="date"
                                value={checkOut}
                                onChange={e => setCheckOut(e.target.value)}
                                required
                            />
                        </label>

                        <label>
                            <span>Personas</span>
                            <input
                                type="number"
                                min="1"
                                value={guests}
                                onChange={e => setGuests(Number(e.target.value))}
                                required
                            />
                        </label>

                        <button className="search-button" disabled={loading}>
                            {loading ? 'Consultando...' : 'Buscar habitaciones'}
                        </button>

                    </form>

                    {error && (
                        <div className="error">
                            {error}
                        </div>
                    )}
                </section>

                {result && (
                    <section className="result-card">

                        <div className="result-header">
                            <div>
                                <span className="eyebrow">
                                    RESULTADO DE LA CONSULTA
                                </span>

                                <h2>
                                    {result.hotel} ·{' '}
                                    {result.room_type.charAt(0).toUpperCase()
                                        + result.room_type.slice(1)}
                                </h2>

                                <p>
                                    {result.check_in} → {result.check_out}
                                    {' · '}
                                    {result.nights} noche(s)
                                </p>
                            </div>

                            <span
                                className={
                                    result.available
                                        ? 'availability available'
                                        : 'availability unavailable'
                                }
                            >
                                {result.available
                                    ? 'Disponible'
                                    : 'No disponible'}
                            </span>
                        </div>

                        <div className="metrics">

                            <div className="metric">
                                <small>Personas</small>
                                <strong>{result.guests}</strong>
                            </div>

                            <div className="metric">
                                <small>Habitaciones necesarias</small>
                                <strong>{result.rooms_required}</strong>
                            </div>

                            <div className="metric">
                                <small>Habitaciones disponibles</small>
                                <strong>{result.available_rooms}</strong>
                            </div>

                            <div className="metric">
                                <small>Capacidad por habitación</small>
                                <strong>{result.capacity_per_room}</strong>
                            </div>

                        </div>

                        {result.available && (
                            <>
                                <div className="price-box">
                                    <div>
                                        <span>Total estimado</span>
                                        <small>
                                            {result.nights} noche(s) · {result.guests} persona(s)
                                        </small>
                                    </div>

                                    <strong>{money(result.total)}</strong>
                                </div>

                                <details className="breakdown">
                                    <summary>Ver detalle de tarifa</summary>

                                    <div className="table-wrapper">
                                        <table>
                                            <thead>
                                                <tr>
                                                    <th>Fecha</th>
                                                    <th>Temporada</th>
                                                    <th>Habitación</th>
                                                    <th>Persona</th>
                                                    <th>Subtotal</th>
                                                </tr>
                                            </thead>

                                            <tbody>
                                                {result.breakdown.map(day => (
                                                    <tr key={day.date}>
                                                        <td>{day.date}</td>
                                                        <td>
                                                            <span className={`season ${day.season}`}>
                                                                {day.season}
                                                            </span>
                                                        </td>
                                                        <td>{money(day.room_rate)}</td>
                                                        <td>{money(day.person_rate)}</td>
                                                        <td>{money(day.subtotal)}</td>
                                                    </tr>
                                                ))}
                                            </tbody>
                                        </table>
                                    </div>
                                </details>
                            </>
                        )}

                    </section>
                )}

                <section className="info-grid">

                    <article>
                        <span>🏨</span>
                        <h3>4 sedes</h3>
                        <p>Barranquilla, Cali, Cartagena y Bogotá.</p>
                    </article>

                    <article>
                        <span>🛏️</span>
                        <h3>3 tipos</h3>
                        <p>Estándar, Premium y VIP según la sede.</p>
                    </article>

                    <article>
                        <span>📅</span>
                        <h3>Disponibilidad real</h3>
                        <p>Se validan cruces de fechas con reservas existentes.</p>
                    </article>

                </section>

            </main>
        </div>
    );
}

createRoot(document.getElementById('root')).render(<App />);
