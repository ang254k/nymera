export function getErrorMessage(error, t) {
    const code = error?.message

    return t(`errors.${code}`, {
        defaultValue: t("errors.request_error"),
    })
}