import MovieCard from '../MovieCard/MovieCard.jsx'
import './MovieList.css'

function MovieList({ movies, favoriteMovies, onToggleFavorite }) {
  return (
    <section className="movie-list" aria-labelledby="movie-list-title">
      <h2 id="movie-list-title">Cartelera</h2>
      <div className="movie-list__grid">
        {movies.map((movie) => (
          <MovieCard
            key={movie.id}
            movie={movie}
            isFavorite={favoriteMovies.some((favoriteMovie) => favoriteMovie.id === movie.id)}
            onToggleFavorite={onToggleFavorite}
          />
        ))}
      </div>
    </section>
  )
}

export default MovieList
