import {
  useRef,
  useState,
} from "react";

import { streamChat } from "../services/chatService";
import type { SSEEvent } from "../types/chat";

export function Chat() {
  const [message, setMessage] = useState("");

  const [response, setResponse] = useState("");

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState<string | null>(
    null
  );

  const abortControllerRef =
    useRef<AbortController | null>(null);

  const handleSubmit = async (
    event: React.FormEvent<HTMLFormElement>
  ) => {
    event.preventDefault();

    const trimmedMessage = message.trim();

    if (!trimmedMessage || loading) {
      return;
    }

    setResponse("");

    setError(null);

    setLoading(true);

    const controller = new AbortController();

    abortControllerRef.current = controller;

    try {
      await streamChat({
        message: trimmedMessage,

        signal: controller.signal,

        onEvent: handleSSEEvent,
      });
    } catch (err) {
      if (
        err instanceof DOMException &&
        err.name === "AbortError"
      ) {
        return;
      }

      const errorMessage =
        err instanceof Error
          ? err.message
          : "Unable to generate AI response.";

      setError(errorMessage);
    } finally {
      setLoading(false);

      abortControllerRef.current = null;
    }
  };

  const handleSSEEvent = (
    event: SSEEvent
  ) => {
    switch (event.event) {
      case "message":
        setResponse(
          (previous) =>
            previous + event.data
        );
        break;

      case "done":
        console.info(
          "AI response completed."
        );
        break;

      case "error":
        setError(event.data);
        break;

      default:
        console.warn(
          "Unknown SSE event:",
          event
        );
    }
  };

  const handleStop = () => {
    abortControllerRef.current?.abort();
  };

  return (
    <div>
      <h1>AI Knowledge Assistant</h1>

      <form onSubmit={handleSubmit}>
        <textarea
          value={message}
          onChange={(event) =>
            setMessage(event.target.value)
          }
          placeholder="Ask something..."
          disabled={loading}
          rows={5}
        />

        <div>
          {!loading ? (
            <button
              type="submit"
              disabled={!message.trim()}
            >
              Send
            </button>
          ) : (
            <button
              type="button"
              onClick={handleStop}
            >
              Stop
            </button>
          )}
        </div>
      </form>

      {error && (
        <div role="alert">
          {error}
        </div>
      )}

      <section>
        <h2>AI Response</h2>

        <div
          style={{
            whiteSpace: "pre-wrap",
          }}
        >
          {response}
          {loading && " ▌"}
        </div>
      </section>
    </div>
  );
}