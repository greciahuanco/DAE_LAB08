import { usePremieres } from '../../hooks/usePremieres.js'
import PremiereSkeleton from './PremiereSkeleton.jsx'
import PremieresCarousel from './PremieresCarousel.jsx'
import './PremieresSection.css'

export default function PremieresSection() {
  const shouldFail = new URLSearchParams(window.location.search).get('premieres') === 'error'
  const { status, data, error } = usePremieres({ shouldFail })

  return (
    <section className="container premieres-section" aria-labelledby="premieres-title">
      <h2 id="premieres-title">Estrenos</h2>
      {status === 'loading' && <PremiereSkeleton />}
      {status === 'success' && <PremieresCarousel movies={data} />}
      {status === 'error' && (
        <p className="status-message status-message--error" role="alert">{error}</p>
      )}
    </section>
  )
}
