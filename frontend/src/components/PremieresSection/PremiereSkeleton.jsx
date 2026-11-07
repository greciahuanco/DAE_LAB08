export default function PremiereSkeleton() {
  return (
    <div role="status">
      <span className="visually-hidden">Cargando estrenos</span>
      <div className="premiere-slide premiere-skeleton" aria-hidden="true">
        <div className="premiere-skeleton__poster" />
        <div className="stack">
          <div className="premiere-skeleton__line premiere-skeleton__line--short" />
          <div className="premiere-skeleton__line" />
          <div className="premiere-skeleton__line" />
        </div>
      </div>
    </div>
  )
}
