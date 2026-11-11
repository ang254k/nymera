import { Link } from "react-router-dom"
import { useTranslation } from "react-i18next"

function Footer() {
  const { i18n } = useTranslation()
  const currentLang = i18n.language || "es"
  const isEs = currentLang.startsWith("es")

  return (
    <footer className="footer">
      <div className="row-center row-wrap" style={{ gap: "var(--space-4)" }}>
        <Link to="/privacy" className="header-link" style={{ fontSize: ".8rem" }}>
          {isEs ? "Política de Privacidad" : "Privacy Policy"}
        </Link>
        
        <span style={{ color: "var(--text-subtle)", fontSize: ".8rem" }}>•</span>
        
        <p className="footer-copy">
          Nymera — {new Date().getFullYear()}
        </p>
        
        <span style={{ color: "var(--text-subtle)", fontSize: ".8rem" }}>•</span>
        
        <Link to="/terms" className="header-link" style={{ fontSize: ".8rem" }}>
          {isEs ? "Términos de Uso" : "Terms of Use"}
        </Link>
      </div>
    </footer>
  )
}

export default Footer