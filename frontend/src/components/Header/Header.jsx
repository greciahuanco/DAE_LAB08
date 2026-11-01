import './Header.css'

function Header() {
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
          <a href="#contacto">Contacto</a>
        </nav>
      </div>
    </header>
  )
}

export default Header

