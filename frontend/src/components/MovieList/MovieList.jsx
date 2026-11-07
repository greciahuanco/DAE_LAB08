import MovieCard from '../MovieCard/MovieCard.jsx'
import { useWindowSize } from '../../hooks/useWindowSize.js'
import './MovieList.css'

function getColumnCount(width) {
  if (width <= 640) return 1
  if (width <= 960) return 2
  return 3
}

function normalizeText(value) {
  return value
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLocaleLowerCase('es')
}

function MovieList({ movies, favoriteMovies, onToggleFavorite, searchText = '' }) {
  const { width } = useWindowSize()
  const columnCount = getColumnCount(width)
  const normalizedSearchText = normalizeText(searchText.trim())
  const matchingMovies = movies.filter((movie) =>
    normalizeText(movie.title).includes(normalizedSearchText),
  )

  return (
    <section className="movie-list" aria-labelledby="movie-list-title">
      <h2 id="movie-list-title">Cartelera</h2>
      {matchingMovies.length > 0 ? (
        <div className="movie-list__grid" style={{ '--movie-columns': columnCount }}>
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
        <p className="status-message" role="status">
          No encontré películas que coincidan con “{searchText}”. Prueba con otro título.
        </p>
      )}
    </section>
  )
}

export default MovieList
