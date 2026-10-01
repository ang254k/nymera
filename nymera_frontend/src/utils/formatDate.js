export function formatDate(date, locale = "es") {
    if (!date) return ""

    const parsedDate = new Date(date)

    if (Number.isNaN(parsedDate.getTime())) return ""

    return new Intl.DateTimeFormat(locale, {
        day: "2-digit",
        month: "2-digit",
        year: "2-digit",
        hour: "2-digit",
        minute: "2-digit"
    }).format(parsedDate)
}