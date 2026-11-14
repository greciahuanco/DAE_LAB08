import './Header.css'

function Header({ favoriteCount }) {
  return (
    <header className="site-header" id="inicio">
      <div className="site-header__content">
        <a className="site-header__brand" href="#inicio">
          Cine Aurora
        </a>
        <nav className="site-header__navigation" aria-label="Navegación principal">
          <a href="#inicio">Inicio</a>
          <a href="#cartelera">Cartelera</a>
          <a href="#promociones">Promociones</a>
          <a href="#exams">Exámenes</a>
          <a href="#contacto">Contacto</a>
        </nav>
        <span className="site-header__favorites">
          <span aria-hidden="true">♥</span> Favoritas: {favoriteCount}
        </span>
      </div>
    </header>
  )
}

export default Header

