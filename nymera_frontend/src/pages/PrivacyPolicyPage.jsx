import { useTranslation } from "react-i18next"
import SEO from "../components/SEO"

function PrivacyPolicyPage() {
    const { i18n } = useTranslation()
    const currentLang = i18n.language || "es"
    const isEs = currentLang.startsWith("es")

    return (
        <div className="page">
            <div className="container-sm stack-lg">
                <SEO 
                    title={isEs ? "Política de Privacidad - Nymera" : "Privacy Policy - Nymera"} 
                    description={isEs ? "Información sobre el tratamiento de datos personales en Nymera conforme al RGPD." : "Information on personal data processing in Nymera according to GDPR."} 
                />

                <header className="stack-sm" style={{ borderBottom: "1px solid var(--border)", paddingBottom: "var(--space-5)" }}>
                    <h1>{isEs ? "Política de Privacidad" : "Privacy Policy"}</h1>
                    <p style={{ color: "var(--text-muted)", fontSize: "0.875rem" }}>
                        {isEs ? "Última actualización: Noviembre 2026" : "Last updated: November 2026"}
                    </p>
                </header>

                <div className="stack" style={{ color: "var(--text-secondary, var(--text))", lineHeight: "1.7" }}>
                    {isEs ? (
                        <>
                            <section className="stack-sm">
                                <h2 style={{ color: "var(--primary)" }}>1. Responsable del Tratamiento</h2>
                                <p>
                                    En <strong>Nymera</strong> respetamos tu privacidad y nos comprometemos a proteger tus datos personales conforme al Reglamento General de Protección de Datos (RGPD). Esta política explica con transparencia qué datos recopilamos y cómo los tratamos.
                                </p>
                            </section>

                            <section className="stack-sm">
                                <h2 style={{ color: "var(--primary)" }}>2. Datos que Recopilamos</h2>
                                <p>Recopilamos estrictamente la información necesaria para el funcionamiento de la plataforma:</p>
                                <ul style={{ paddingLeft: "var(--space-5)", display: "flex", flexDirection: "column", gap: "var(--space-2)" }}>
                                    <li><strong>Datos de cuenta:</strong> Nombre de usuario, correo electrónico y contraseña encriptada mediante hash seguro.</li>
                                    <li><strong>Perfil:</strong> Imagen de avatar alojada y gestionada de forma segura en la nube (Cloudinary).</li>
                                    <li><strong>Contenido:</strong> Sueños publicados, comentarios, etiquetas y reacciones ("me gusta").</li>
                                    <li><strong>Seguridad:</strong> Registros técnicos y direcciones IP anonimizadas/minimizadas exclusivamente para la prevención de abusos y protección de la plataforma (`security_logs`).</li>
                                </ul>
                            </section>

                            <section className="stack-sm">
                                <h2 style={{ color: "var(--primary)" }}>3. Cookies y Almacenamiento Local</h2>
                                <p>
                                    Nymera no utiliza cookies de publicidad ni herramientas de analítica invasiva de terceros. Únicamente empleamos:
                                </p>
                                <ul style={{ paddingLeft: "var(--space-5)", display: "flex", flexDirection: "column", gap: "var(--space-2)" }}>
                                    <li><strong>Cookies HTTP-Only:</strong> Utilizadas exclusivamente para mantener la sesión segura del usuario.</li>
                                    <li><strong>Almacenamiento local (`localStorage`):</strong> Empleado únicamente para recordar tu preferencia de idioma en la interfaz.</li>
                                </ul>
                            </section>

                            <section className="stack-sm">
                                <h2 style={{ color: "var(--primary)" }}>4. Borrado de Cuenta y Derecho al Olvido</h2>
                                <p>
                                    Puedes eliminar tu cuenta de forma autónoma en cualquier momento desde los ajustes de tu perfil. Al ejecutar el borrado:
                                </p>
                                <ul style={{ paddingLeft: "var(--space-5)", display: "flex", flexDirection: "column", gap: "var(--space-2)" }}>
                                    <li>Tus datos personales, avatar, comentarios, notificaciones y likes se eliminan permanentemente de la base de datos y de la nube.</li>
                                    <li>Tus sueños publicados se conservan para mantener la coherencia de la comunidad, pero quedan <strong>completamente anonimizados</strong> (desvinculados de tu usuario).</li>
                                </ul>
                            </section>

                            <section className="stack-sm">
                                <h2 style={{ color: "var(--primary)" }}>5. Tus Derechos</h2>
                                <p>
                                    Tienes derecho a acceder, rectificar, limitar o solicitar la supresión completa de tus datos personales gestionando tu perfil directamente en la plataforma.
                                </p>
                            </section>
                        </>
                    ) : (
                        <>
                            <section className="stack-sm">
                                <h2 style={{ color: "var(--primary)" }}>1. Data Controller</h2>
                                <p>
                                    At <strong>Nymera</strong>, we respect your privacy and are committed to protecting your personal data in compliance with the General Data Protection Regulation (GDPR).
                                </p>
                            </section>

                            <section className="stack-sm">
                                <h2 style={{ color: "var(--primary)" }}>2. Data We Collect</h2>
                                <p>We strictly gather the data required to operate the platform:</p>
                                <ul style={{ paddingLeft: "var(--space-5)", display: "flex", flexDirection: "column", gap: "var(--space-2)" }}>
                                    <li><strong>Account details:</strong> Username, email address, and securely hashed password.</li>
                                    <li><strong>Profile:</strong> Avatar image safely stored and managed in the cloud (Cloudinary).</li>
                                    <li><strong>Content:</strong> Published dreams, comments, tags, and likes.</li>
                                    <li><strong>Security:</strong> Minimized technical logs and IP addresses strictly used for platform protection (`security_logs`).</li>
                                </ul>
                            </section>

                            <section className="stack-sm">
                                <h2 style={{ color: "var(--primary)" }}>3. Cookies and Local Storage</h2>
                                <p>
                                    Nymera does not use advertising cookies or invasive third-party analytics. We only use:
                                </p>
                                <ul style={{ paddingLeft: "var(--space-5)", display: "flex", flexDirection: "column", gap: "var(--space-2)" }}>
                                    <li><strong>HTTP-Only Cookies:</strong> Exclusively used to maintain secure user sessions.</li>
                                    <li><strong>Local Storage (`localStorage`):</strong> Used solely to remember your UI language preference.</li>
                                </ul>
                            </section>

                            <section className="stack-sm">
                                <h2 style={{ color: "var(--primary)" }}>4. Account Deletion and Right to be Forgotten</h2>
                                <p>
                                    You can delete your account at any time from your profile settings. Upon deletion:
                                </p>
                                <ul style={{ paddingLeft: "var(--space-5)", display: "flex", flexDirection: "column", gap: "var(--space-2)" }}>
                                    <li>Your personal data, avatar, comments, notifications, and likes are permanently deleted from our database and cloud storage.</li>
                                    <li>Your published dreams remain to preserve community continuity, but are <strong>completely anonymized</strong> (unlinked from your profile).</li>
                                </ul>
                            </section>

                            <section className="stack-sm">
                                <h2 style={{ color: "var(--primary)" }}>5. Your Rights</h2>
                                <p>
                                    You have the right to access, rectify, restrict, or request the complete erasure of your personal data directly through your profile settings.
                                </p>
                            </section>
                        </>
                    )}
                </div>
            </div>
        </div>
    )
}

export default PrivacyPolicyPage