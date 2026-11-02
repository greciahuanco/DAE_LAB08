import { useState } from 'react'
import Footer from './components/Footer/Footer.jsx'
import Header from './components/Header/Header.jsx'
import Hero from './components/Hero/Hero.jsx'
import MovieList from './components/MovieList/MovieList.jsx'
import { movies } from './data/movies.js'

function App() {
  const [favoriteMovies, setFavoriteMovies] = useState([])

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

  return (
    <>
      <Header />
      <main id="cartelera">
        <Hero movie={movies[0]} />
        <MovieList
          movies={movies}
          favoriteMovies={favoriteMovies}
          onToggleFavorite={toggleFavorite}
        />
      </main>
      <Footer />
    </>
  )
}

export default App
