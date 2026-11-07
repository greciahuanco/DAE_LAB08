import { useState } from 'react'
import Button from '../Button/Button.jsx'

export default function PremieresCarousel({ movies }) {
  const [activeIndex, setActiveIndex] = useState(0)
  const movie = movies[activeIndex]

  function moveSlide(offset) {
    setActiveIndex((index) => (index + offset + movies.length) % movies.length)
  }

  return (
    <div role="group" aria-roledescription="carrusel" aria-label="Películas de estreno">
      <div className="premiere-slide" aria-live="polite">
        <img className="premiere-slide__poster" src={movie.image} alt={`Póster de ${movie.title}`} />
        <div>
          <h3>{movie.title}</h3>
          <p>{movie.synopsis}</p>
          <p className="text-muted">{activeIndex + 1} de {movies.length}</p>
        </div>
      </div>
      <div className="cluster premieres-controls">
        <Button variant="secondary" onClick={() => moveSlide(-1)}>Anterior</Button>
        <Button variant="secondary" onClick={() => moveSlide(1)}>Siguiente</Button>
      </div>
    </div>
  )
}
