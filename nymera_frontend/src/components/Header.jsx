import { useEffect, useState } from "react"
import { Link, useNavigate, useLocation } from "react-router-dom"

import { APP_NAME, APP_ICON } from "../config/app"

import { Home, Bell, User, LogOut } from "../lib/icons"

import { useAuth } from "../context/AuthContext"
import { getNotificaciones } from "../api/notificaciones"
import { useToast } from "../context/ToastContext"

function Header() {
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
    showToast("Sesión cerrada", "info")
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
          aria-label={`${APP_NAME}, ir al inicio`}
        >
          <Home size={18} />
          <span className="header-link-text">
            Inicio
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
                Salir
              </span>
            </button>

          </>
        ) : (
          <>
            <Link className="header-link" to="/login">
              Login
            </Link>
            <Link
              className="btn btn-primary btn-sm"
              to="/register">
              Registro
            </Link>
          </>
        )}

      </nav>

    </header>
  )
}

export default Header