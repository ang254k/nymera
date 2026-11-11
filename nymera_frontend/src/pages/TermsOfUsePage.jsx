import { useTranslation } from "react-i18next"
import SEO from "../components/SEO"

function TermsOfUsePage() {
    const { i18n } = useTranslation()
    const currentLang = i18n.language || "es"
    const isEs = currentLang.startsWith("es")

    return (
        <div className="page">
            <div className="container-sm stack-lg">
                <SEO 
                    title={isEs ? "Términos de Uso - Nymera" : "Terms of Use - Nymera"} 
                    description={isEs ? "Condiciones generales de uso de la plataforma y comunidad Nymera." : "General terms and conditions of use for the Nymera platform and community."} 
                />

                <header className="stack-sm" style={{ borderBottom: "1px solid var(--border)", paddingBottom: "var(--space-5)" }}>
                    <h1>{isEs ? "Términos de Uso" : "Terms of Use"}</h1>
                    <p style={{ color: "var(--text-muted)", fontSize: "0.875rem" }}>
                        {isEs ? "Última actualización: Noviembre 2026" : "Last updated: November 2026"}
                    </p>
                </header>

                <div className="stack" style={{ color: "var(--text-secondary, var(--text))", lineHeight: "1.7" }}>
                    {isEs ? (
                        <>
                            <section className="stack-sm">
                                <h2 style={{ color: "var(--primary)" }}>1. Aceptación de los Términos</h2>
                                <p>
                                    Al acceder, registrarte o utilizar <strong>Nymera</strong>, aceptas cumplir y quedar vinculado por estos Términos de Uso. Si no estás de acuerdo con alguna parte de las condiciones, no debes utilizar la plataforma.
                                </p>
                            </section>

                            <section className="stack-sm">
                                <h2 style={{ color: "var(--primary)" }}>2. Registro y Seguridad de la Cuenta</h2>
                                <p>
                                    Para interactuar en la comunidad, publicar sueños o dejar comentarios, debes registrarte creando una cuenta de usuario. Eres responsable de mantener la confidencialidad de tu contraseña y de toda la actividad que ocurra bajo tu cuenta.
                                </p>
                            </section>

                            <section className="stack-sm">
                                <h2 style={{ color: "var(--primary)" }}>3. Conducta del Usuario y Normas de la Comunidad</h2>
                                <p>Nymera es un espacio seguro dedicado a compartir y explorar el mundo de los sueños. Te comprometes a <strong>no</strong> utilizar la plataforma para:</p>
                                <ul style={{ paddingLeft: "var(--space-5)", display: "flex", flexDirection: "column", gap: "var(--space-2)" }}>
                                    <li>Publicar contenido ilegal, difamatorio, acosador, amenazante, racista o explícitamente violento.</li>
                                    <li>Infringir derechos de propiedad intelectual de terceros.</li>
                                    <li>Intentar vulnerar la seguridad del sistema, realizar ataques de denegación de servicio o extraer datos automatizados de forma masiva (web scraping abusivo).</li>
                                </ul>
                            </section>

                            <section className="stack-sm">
                                <h2 style={{ color: "var(--primary)" }}>4. Propiedad Intelectual y Contenido del Usuario</h2>
                                <p>
                                    <strong>Propiedad de la Plataforma:</strong> El código fuente, el diseño visual, las interfaces, los logotipos y la estructura general de Nymera son propiedad exclusiva de los creadores de la plataforma y están protegidos por las leyes de propiedad intelectual aplicables.
                                </p>
                                <p>
                                    <strong>Contenido del Usuario:</strong> Conservas la propiedad absoluta de lo que escribes. Los sueños, relatos y comentarios que publicas en Nymera te pertenecen. Al publicarlos, otorgas a la plataforma una licencia técnica, mundial y no exclusiva estrictamente necesaria para alojar, mostrar y procesar dicho contenido dentro de la comunidad conforme a la configuración de visibilidad que selecciones.
                                </p>
                                <p>
                                    <strong>Reclamaciones de Copyright:</strong> Si consideras que algún contenido publicado en la plataforma infringe derechos de propiedad intelectual ajenos, puedes notificarlo a través de los canales internos de soporte o contacto habilitados en la aplicación para proceder a su revisión y retirada si procede.
                                </p>
                            </section>

                            <section className="stack-sm">
                                <h2 style={{ color: "var(--primary)" }}>5. Modificaciones y Terminación</h2>
                                <p>
                                    Nos reservamos el derecho de modificar estos términos en cualquier momento. Asimismo, podemos suspender o cancelar cuentas de usuario que incumplan de forma grave o reiterada estas normas de convivencia.
                                </p>
                            </section>
                        </>
                    ) : (
                        <>
                            <section className="stack-sm">
                                <h2 style={{ color: "var(--primary)" }}>1. Acceptance of Terms</h2>
                                <p>
                                    By accessing, registering, or using <strong>Nymera</strong>, you agree to comply with and be bound by these Terms of Use. If you disagree with any part of these terms, you must not use the platform.
                                </p>
                            </section>

                            <section className="stack-sm">
                                <h2 style={{ color: "var(--primary)" }}>2. Account Registration and Security</h2>
                                <p>
                                    To interact within the community, publish dreams, or leave comments, you must register by creating a user account. You are responsible for maintaining the confidentiality of your password and for all activities under your account.
                                </p>
                            </section>

                            <section className="stack-sm">
                                <h2 style={{ color: "var(--primary)" }}>3. User Conduct and Community Guidelines</h2>
                                <p>Nymera is a safe space dedicated to sharing and exploring dreams. You agree <strong>not</strong> to use the platform to:</p>
                                <ul style={{ paddingLeft: "var(--space-5)", display: "flex", flexDirection: "column", gap: "var(--space-2)" }}>
                                    <li>Publish illegal, defamatory, harassing, threatening, racist, or explicitly violent content.</li>
                                    <li>Infringe third-party intellectual property rights.</li>
                                    <li>Attempt to compromise system security, perform denial-of-service attacks, or execute unauthorized automated data scraping.</li>
                                </ul>
                            </section>

                            <section className="stack-sm">
                                <h2 style={{ color: "var(--primary)" }}>4. Intellectual Property and User Content</h2>
                                <p>
                                    <strong>Platform Ownership:</strong> The source code, visual design, interfaces, logos, and overall structure of Nymera are the exclusive property of the platform creators and are protected by applicable intellectual property laws.
                                </p>
                                <p>
                                    <strong>User Content:</strong> You retain full ownership of what you write. The dreams, stories, and comments you post on Nymera belong to you. By publishing them, you grant the platform a non-exclusive, worldwide technical license strictly necessary to host, display, and process such content within the community according to your chosen visibility settings.
                                </p>
                                <p>
                                    <strong>Copyright Claims:</strong> If you believe that any content published on the platform infringes third-party intellectual property rights, you can report it through the internal support or contact channels provided within the application for review and potential removal.
                                </p>
                            </section>

                            <section className="stack-sm">
                                <h2 style={{ color: "var(--primary)" }}>5. Modifications and Termination</h2>
                                <p>
                                    We reserve the right to modify these terms at any time. We also reserve the right to suspend or terminate user accounts that seriously or repeatedly violate these community guidelines.
                                </p>
                            </section>
                        </>
                    )}
                </div>
            </div>
        </div>
    )
}

export default TermsOfUsePage