import { useEffect, useState } from 'react'
import Footer from './components/Footer/Footer.jsx'
import Header from './components/Header/Header.jsx'
import Hero from './components/Hero/Hero.jsx'
import MovieList from './components/MovieList/MovieList.jsx'
import PremieresSection from './components/PremieresSection/PremieresSection.jsx'
import { movies } from './data/movies.js'
import { useDebounce } from './hooks/useDebounce.js'
import './styles/favorite-notice.css'

const searchDelay = 400
const favoritesStorageKey = 'cine-aurora-favorites'

function loadFavoriteMovies() {
  try {
    const savedFavorites = window.localStorage.getItem(favoritesStorageKey)
    const parsedFavorites = savedFavorites ? JSON.parse(savedFavorites) : []

    return Array.isArray(parsedFavorites) ? parsedFavorites : []
  } catch {
    return []
  }
}

function App() {
  const [favoriteMovies, setFavoriteMovies] = useState(loadFavoriteMovies)
  const [favoriteNotice, setFavoriteNotice] = useState(null)
  const [searchText, setSearchText] = useState('')
  const debouncedSearchText = useDebounce(searchText, searchDelay)
  const favoriteCount = favoriteMovies.length

  useEffect(() => {
    window.localStorage.setItem(favoritesStorageKey, JSON.stringify(favoriteMovies))
  }, [favoriteMovies])

  useEffect(() => {
    if (!favoriteNotice) return

    const timer = window.setTimeout(() => setFavoriteNotice(null), 4000)
    return () => window.clearTimeout(timer)
  }, [favoriteNotice])

  function handleSearchChange(event) {
    setSearchText(event.target.value)
  }

  function toggleFavorite(movie) {
    const isFavorite = favoriteMovies.some((favoriteMovie) => favoriteMovie.id === movie.id)
    const nextFavorites = isFavorite
      ? favoriteMovies.filter((favoriteMovie) => favoriteMovie.id !== movie.id)
      : [...favoriteMovies, movie]

    setFavoriteMovies(nextFavorites)
    setFavoriteNotice({
      message: isFavorite
        ? `Quitaste «${movie.title}» de tus favoritas`
        : `Agregaste «${movie.title}» a tus favoritas`,
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
      <Header favoriteCount={favoriteCount} />
      <main id="cartelera">
        <Hero
          movie={movies[0]}
          searchValue={searchText}
          onSearchChange={handleSearchChange}
          onShowMovies={handleShowMovies}
        />
        <PremieresSection />
        <MovieList
          movies={movies}
          favoriteMovies={favoriteMovies}
          onToggleFavorite={toggleFavorite}
          searchText={debouncedSearchText}
        />
      </main>
      <Footer />
      <div className="favorite-notice" role="status">
        {favoriteNotice && <p>{favoriteNotice.message}</p>}
      </div>
    </>
  )
}

export default App
