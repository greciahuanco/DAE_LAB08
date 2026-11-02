import Button from '../Button/Button.jsx'
import MovieSearch from '../MovieSearch/MovieSearch.jsx'
import './Hero.css'

function Hero({ movie, searchValue, onSearchChange, onShowMovies }) {
  return (
    <section className="featured-movie" aria-labelledby="featured-movie-title">
      <div className="featured-movie__content">
        <p className="featured-movie__eyebrow">Película destacada</p>
        <h1 id="featured-movie-title">{movie.title}</h1>
        <p className="featured-movie__synopsis">{movie.synopsis}</p>
        <div className="featured-movie__details">
          <span>{movie.classification}</span>
          <span className="featured-movie__rating">★ {movie.rating}/10</span>
        </div>
        <p className="featured-movie__showtimes">
          <strong>Horarios:</strong> {movie.showtimes.join(' · ')}
        </p>
        <div className="featured-movie__search">
          <MovieSearch value={searchValue} onChange={onSearchChange} />
          <Button onClick={onShowMovies}>Ver resultados</Button>
        </div>
      </div>
      <div className="featured-movie__poster">
        <img src={movie.image} alt={`Póster de ${movie.title}`} />
      </div>
    </section>
  )
}

export default Hero
