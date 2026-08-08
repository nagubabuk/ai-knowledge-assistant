
def format_sse_event(
    data: str,
    event: str = "message",
) -> str:

    return f"event: {event}\ndata: {data}\n\n"