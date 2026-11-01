import Footer from './components/Footer/Footer.jsx'
import Header from './components/Header/Header.jsx'
import Hero from './components/Hero/Hero.jsx'
import MovieList from './components/MovieList/MovieList.jsx'
import { movies } from './data/movies.js'

function App() {
  const featuredMovie = movies[0]

  return (
    <>
      <Header />
      <main id="cartelera">
        <Hero movie={featuredMovie} />
        <MovieList movies={movies} />
      </main>
      <Footer />
    </>
  )
}

export default App
