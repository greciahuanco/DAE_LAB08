import Footer from './components/Footer/Footer.jsx'
import Header from './components/Header/Header.jsx'
import Hero from './components/Hero/Hero.jsx'
import { movies } from './data/movies.js'

function App() {
  return (
    <>
      <Header />
      <main id="cartelera">
        <Hero movie={movies[0]} />
      </main>
      <Footer />
    </>
  )
}

export default App
