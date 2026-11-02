import './MovieSearch.css'

function MovieSearch({ value, onChange }) {
  return (
    <div className="movie-search">
      <label className="form-label" htmlFor="movie-search-input">
        Buscar películas
      </label>
      <input
        className="form-control"
        id="movie-search-input"
        type="search"
        value={value}
        onChange={onChange}
        placeholder="Escribe el título de una película"
        autoComplete="off"
      />
    </div>
  )
}

export default MovieSearch
