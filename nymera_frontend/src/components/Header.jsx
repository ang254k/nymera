import { useEffect, useState } from "react"
import { useTranslation } from "react-i18next"
import { Link, useNavigate, useLocation } from "react-router-dom"

import { APP_NAME, APP_ICON } from "../config/app"
import banderaES from "../assets/flags/es.svg"
import banderaEN from "../assets/flags/en.svg"

import { Home, Bell, User, LogOut } from "../lib/icons"

import { useAuth } from "../context/AuthContext"
import { getNotificaciones } from "../api/notificaciones"
import { useToast } from "../context/ToastContext"

function Header() {
  const { t, i18n } = useTranslation()

  const { user, logoutUser } = useAuth()

  const navigate = useNavigate()
  const location = useLocation()
  const { showToast } = useToast()

  const [count, setCount] = useState(0)
  const [langAnimating, setLangAnimating] = useState(false)
  const isSpanish = i18n.language.startsWith("es")

  useEffect(() => {
    async function load() {
      if (!user || location.pathname === "/login" || location.pathname === "/register")
        return

      try {
        const data = await getNotificaciones()
        const noLeidas = data.filter(n => !n.leido).length
        setCount(noLeidas)
      } catch (err) {
        setCount(0)
      }
    }
    load()
  }, [user, location.pathname])

  useEffect(() => {
    function handleNotificacionesActualizadas(e) {
      if (typeof e.detail?.count === "number") {
        setCount(e.detail.count)
      }
    }

    window.addEventListener("notificacionesActualizadas", handleNotificacionesActualizadas)
    return () => {
      window.removeEventListener("notificacionesActualizadas", handleNotificacionesActualizadas)
    }
  }, [])

  function handleLogout() {
    setCount(0)
    showToast(t("messages.logoutSuccess"), "info")
    logoutUser()
    navigate("/login")
  }

  function handleToggleLanguage() {
    const nextLang = i18n.language.startsWith("es") ? "en" : "es"
    setLangAnimating(true)
    i18n.changeLanguage(nextLang)
  }

  return (
    <header className="header">

      <Link
        to="/home"
        className="header-brand"
        aria-label={`${APP_NAME}, ${t("accessibility.goHome")}`}
      >
        <img
          src={APP_ICON}
          alt={APP_NAME}
          className="brand-icon"
        />

      </Link>

      <nav className="header-nav">

        <Link
          className="header-link"
          to="/home"
          aria-label={`${APP_NAME}, ${t("accessibility.goHome")}`}
        >
          <Home size={18} />
          <span className="header-link-text">
            {t("navigation.home")}
          </span>

        </Link>

        {user ? (
          <>
            <Link
              className="header-link notification-link"
              to="/notificaciones"
              aria-label={
                count > 0
                  ? t("navigation.notificationsCount", { count })
                  : t("navigation.notifications")
              }
            >
              {/* Notificaciones */}
              <Bell size={18} />

              {count > 0 && (
                <span className="notification-badge">
                  {count}
                </span>
              )}
            </Link>

            <Link
              className="header-link"
              to="/perfil"
            >
              <User size={18} />

              <span className="header-link-text">
                {user.nombre}
              </span>
            </Link>

            <button
              type="button"
              className="btn btn-secondary btn-sm"
              onClick={handleLogout}
            >
              <LogOut size={16} />
              <span className="header-link-text">
                {t("navigation.logout")}
              </span>
            </button>


          </>
        ) : (
          <>
            <Link
              className="header-link"
              to="/login"
              aria-label={t("navigation.login")}
            >
              <span>
                {t("navigation.login")}
              </span>
            </Link>

            <Link
              className="btn btn-primary btn-sm"
              to="/register">
              {t("navigation.register")}
            </Link>
          </>
        )}

        <div className="language-switcher">
          <button
            type="button"
            className={`language-toggle-btn ${langAnimating ? "is-animating" : ""}`}
            onClick={handleToggleLanguage}
            onAnimationEnd={() => setLangAnimating(false)}
            aria-label={
              isSpanish
                ? t("language.englishLanguage")
                : t("language.spanishLanguage")
            }
            title={isSpanish ? "Cambiar a English" : "Switch to Español"}
          >
            <img
              src={isSpanish ? banderaES : banderaEN}
              alt=""
            />
          </button>
        </div>

      </nav>

    </header>
  )
}

export default Header