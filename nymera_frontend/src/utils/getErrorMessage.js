export function getErrorMessage(error, t) {
    const code = error?.message

    if (code?.startsWith("verification_resend_cooldown:")) {
        const seconds = code.split(":")[1]
        return t("errors.verification_resend_cooldown", { seconds })
    }
    
    return t(`errors.${code}`, {
        defaultValue: t("errors.request_error"),
    })
}