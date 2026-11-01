import './Footer.css'

function Footer() {
  return (
    <footer className="site-footer" id="contacto">
      <div className="site-footer__content">
        <section className="site-footer__brand" aria-labelledby="footer-title">
          <h2 id="footer-title">Cine Aurora</h2>
          <p>Disfruta tus historias favoritas en pantalla grande.</p>
        </section>
        <section className="site-footer__contact" aria-labelledby="contact-title">
          <h2 id="contact-title">Contacto e información</h2>
          <address>
            <a href="mailto:contacto@cineaurora.com">contacto@cineaurora.com</a>
            <span>Lima, Perú</span>
            <span>Atención todos los días, de 13:00 a 23:00</span>
          </address>
        </section>
        <p className="site-footer__copyright">
          Cine Aurora. Todos los derechos reservados.
        </p>
      </div>
    </footer>
  )
}

export default Footer

