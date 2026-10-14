def format_sse_event(
    data: str,
    event: str = "message",
) -> str:
    """
    Format data according to the SSE protocol.

    Each line of a multi-line data payload must
    be prefixed with `data:`.
    """

    lines = data.splitlines() or [""]

    formatted_data = "\n".join(
        f"data: {line}"
        for line in lines
    )

    return (
        f"event: {event}\n"
        f"{formatted_data}\n\n"
    )