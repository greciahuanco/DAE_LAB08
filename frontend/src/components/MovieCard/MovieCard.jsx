import './MovieCard.css'

function MovieCard({ movie }) {
  return (
    <article className="movie-card">
      <img
        className="movie-card__poster"
        src={movie.image}
        alt={`Póster de ${movie.title}`}
        loading="lazy"
      />
      <div className="movie-card__content">
        <h3>{movie.title}</h3>
        <p className="movie-card__rating" aria-label={`Valoración ${movie.rating} de 10`}>
          <span aria-hidden="true">★</span> {movie.rating}/10
        </p>
        <div className="movie-card__showtimes">
          <h4>Horarios</h4>
          <ul>
            {movie.showtimes.map((showtime) => (
              <li key={showtime}>{showtime}</li>
            ))}
          </ul>
        </div>
      </div>
    </article>
  )
}

export default MovieCard
