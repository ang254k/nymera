import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'

import "./i18n"

import "./styles/theme.css";
import "./styles/global.css";
import "./styles/layout.css";
import "./styles/forms.css";
import "./styles/buttons.css";
import "./styles/cards.css";
import "./styles/components.css";
import "./styles/animation.css";
import "./styles/layouts.css";
 
import App from './App.jsx'

import { AuthProvider } from './context/AuthContext'
import { ToastProvider } from './context/ToastContext.jsx'
import { DreamFilterProvider } from './context/DreamFilterContext.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <AuthProvider>
      <ToastProvider>
        <DreamFilterProvider>
          <App />
        </DreamFilterProvider>
      </ToastProvider>
    </AuthProvider>
  </StrictMode>,
)
