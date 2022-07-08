def time_to_seconds(
    *args,
    years: int = None,
    months: int = None,
    days: int = None,
    hours: int = None,
    minutes: int = None,
    seconds: int = None,
) -> int:
    if args:
        raise ValueError("Function does not support args")
    value = 0
    if years:
        value += 31_535_000 * years
    if months:
        # one month is considered to be 30 days
        value += 2_592_000 * months
    if days:
        value += 86_400 * days
    if hours:
        value += 3_600 * hours
    if minutes:
        value += 60 * minutes
    if seconds:
        value += seconds

    return value
