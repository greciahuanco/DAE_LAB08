import { useEffect, useRef, useState } from 'react'
import Footer from './components/Footer/Footer.jsx'
import Header from './components/Header/Header.jsx'
import Hero from './components/Hero/Hero.jsx'
import MovieList from './components/MovieList/MovieList.jsx'
import { movies } from './data/movies.js'

const searchDelay = 400

function App() {
  const [favoriteMovies, setFavoriteMovies] = useState([])
  const [searchText, setSearchText] = useState('')
  const [debouncedSearchText, setDebouncedSearchText] = useState('')
  const searchTimer = useRef(null)

  useEffect(() => () => window.clearTimeout(searchTimer.current), [])

  function handleSearchChange(event) {
    const nextSearchText = event.target.value
    setSearchText(nextSearchText)
    console.log('Texto escrito:', nextSearchText)

    window.clearTimeout(searchTimer.current)
    searchTimer.current = window.setTimeout(() => {
      setDebouncedSearchText(nextSearchText)
      console.log('Texto procesado después del retardo:', nextSearchText)
    }, searchDelay)
  }

  function toggleFavorite(movie) {
    setFavoriteMovies((currentFavorites) => {
      const isFavorite = currentFavorites.some(
        (favoriteMovie) => favoriteMovie.id === movie.id,
      )

      if (isFavorite) {
        return currentFavorites.filter((favoriteMovie) => favoriteMovie.id !== movie.id)
      }

      return [...currentFavorites, movie]
    })
  }

  function handleShowMovies() {
    document.getElementById('movie-list-title')?.scrollIntoView({
      behavior: 'smooth',
      block: 'start',
    })
  }

  return (
    <>
      <Header />
      <main id="cartelera">
        <Hero
          movie={movies[0]}
          searchValue={searchText}
          onSearchChange={handleSearchChange}
          onShowMovies={handleShowMovies}
        />
        <MovieList
          movies={movies}
          favoriteMovies={favoriteMovies}
          onToggleFavorite={toggleFavorite}
          searchText={debouncedSearchText}
        />
      </main>
      <Footer />
    </>
  )
}

export default App
