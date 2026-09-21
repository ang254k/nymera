import { BrowserRouter, Routes, Route } from "react-router-dom"

import RegisterPage from "./pages/RegisterPage"
import LoginPage from "./pages/LoginPage"
import FeedPage from "./pages/FeedPage"
import SuenoDetallePage from "./pages/SuenoDetallePage"
import PerfilPage from "./pages/PerfilPage"
import NotificacionesPage from "./pages/NotificacionesPage"
import UsuarioPage from "./pages/UsuarioPage"
import BusquedaPage from "./pages/BusquedaPage"
import HashtagPage from "./pages/HashtagPage"
import LayoutPrivado from "./components/LayoutPrivado"
import LayoutPublico from "./components/LayoutPublico"
import ResetPasswordPage from "./pages/ResetPasswordPage"
import ForgotPasswordPage from "./pages/ForgotPasswordPage"
import ProtectedRoute from "./components/ProtectedRoute"
import ErrorPage from "./pages/ErrorPage"
import NymeraBackground from "./components/NymeraBackground"

function App() {
  return (
    <BrowserRouter>
      <NymeraBackground />
        <Routes>
          <Route element={<LayoutPublico />}>
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/reset-password/:token" element={<ResetPasswordPage />} />
            <Route path="/forgot-password" element={<ForgotPasswordPage />} />

          </Route>
          <Route element={<LayoutPrivado />}>
            <Route path="/home" element={<FeedPage />} />
            <Route
              path="/perfil"
              element={
                <ProtectedRoute>
                  <PerfilPage />
                </ProtectedRoute>
              }
            />
            <Route path="/suenos/:id" element={<SuenoDetallePage />} />
            <Route
              path="/notificaciones"
              element={
                <ProtectedRoute>
                  <NotificacionesPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/usuarios/:id"
              element={
                <ProtectedRoute>
                  <UsuarioPage />
                </ProtectedRoute>
              }
            />
            <Route path="/search" element={<BusquedaPage />} />
            <Route path="/hashtags/:nombre" element={<HashtagPage />} />
          </Route>

          <Route path="*" element={<ErrorPage />} />

        </Routes>

    </BrowserRouter>
  )
}

export default App