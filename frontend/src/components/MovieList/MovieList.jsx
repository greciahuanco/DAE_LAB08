import MovieCard from '../MovieCard/MovieCard.jsx'
import './MovieList.css'

function normalizeText(value) {
  return value
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLocaleLowerCase('es')
}

function MovieList({ movies, favoriteMovies, onToggleFavorite, searchText = '' }) {
  const normalizedSearchText = normalizeText(searchText.trim())
  const matchingMovies = movies.filter((movie) =>
    normalizeText(movie.title).includes(normalizedSearchText),
  )

  return (
    <section className="movie-list" aria-labelledby="movie-list-title">
      <h2 id="movie-list-title">Cartelera</h2>
      {matchingMovies.length > 0 ? (
        <div className="movie-list__grid">
          {matchingMovies.map((movie) => (
            <MovieCard
              key={movie.id}
              movie={movie}
              isFavorite={favoriteMovies.some((favoriteMovie) => favoriteMovie.id === movie.id)}
              onToggleFavorite={onToggleFavorite}
            />
          ))}
        </div>
      ) : (
        <p className="movie-list__empty" role="status">
          No encontré películas que coincidan con “{searchText}”. Prueba con otro título.
        </p>
      )}
    </section>
  )
}

export default MovieList
