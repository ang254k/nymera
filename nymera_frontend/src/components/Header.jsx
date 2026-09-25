import { useEffect, useState } from "react"
import { useTranslation } from "react-i18next"

import { Link, useNavigate, useLocation } from "react-router-dom"

import { APP_NAME, APP_ICON } from "../config/app"

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

  useEffect(() => {
    async function load() {
      if (!user) return

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

  function handleLogout() {
    setCount(0)
    showToast(t("messages.logoutSuccess"), "info")
    logoutUser()
    navigate("/login")
  }

  return (
    <header className="header">

      <Link
        to="/home"
        className="header-brand"
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
            <Link className="header-link" to="/login">
              {t("navigation.login")}
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
            onClick={() => i18n.changeLanguage("es")}
          >
            ES
          </button>

          <span>|</span>

          <button
            type="button"
            onClick={() => i18n.changeLanguage("en")}
          >
            EN
          </button>
        </div>

      </nav>

    </header>
  )
}

export default Header