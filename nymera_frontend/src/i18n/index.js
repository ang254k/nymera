import i18n from "i18next"
import { initReactI18next } from "react-i18next"
import LanguageDetector from "i18next-browser-languagedetector"

import es from "./locales/es.json"
import en from "./locales/en.json"

i18n
    .use(initReactI18next)
    .use(LanguageDetector)
    .init({
        resources: {
            es: {
                translation: es,
            },
            en: {
                translation: en,
            },
        },

        detection: {
            order: ["localStorage", "navigator"],
            caches: ["localStorage"],
        },
        
        fallbackLng: "es",
    })