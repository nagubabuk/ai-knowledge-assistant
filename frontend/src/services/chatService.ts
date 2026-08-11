import { SSEParser } from "../utils/sseParser";
import type { SSEEvent } from "../types/chat";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL;

if (!API_BASE_URL) {
  throw new Error(
    "VITE_API_BASE_URL is not configured."
  );
}

export interface StreamChatOptions {
  message: string;
  signal?: AbortSignal;
  onEvent: (event: SSEEvent) => void;
}

export async function streamChat({
  message,
  signal,
  onEvent,
}: StreamChatOptions): Promise<void> {
  const response = await fetch(
    `${API_BASE_URL}/chat/stream`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
        Accept: "text/event-stream",
      },

      body: JSON.stringify({
        message,
      }),

      signal,
    }
  );

  if (!response.ok) {
    throw new Error(
      `Chat request failed with status ${response.status}`
    );
  }

  if (!response.body) {
    throw new Error(
      "Streaming response body is not available."
    );
  }

  const reader = response.body.getReader();

  const decoder = new TextDecoder("utf-8");

  const parser = new SSEParser();

  try {
    while (true) {
      const { done, value } = await reader.read();

      if (done) {
        break;
      }

      const decodedChunk = decoder.decode(value, {
        stream: true,
      });

      const events = parser.feed(decodedChunk);

      for (const event of events) {
        onEvent(event);
      }
    }

    // Flush any remaining decoder bytes.
    const remainingText = decoder.decode();

    if (remainingText) {
      const events = parser.feed(remainingText);

      for (const event of events) {
        onEvent(event);
      }
    }

    // Process any final buffered SSE event.
    const finalEvents = parser.end();

    for (const event of finalEvents) {
      onEvent(event);
    }
  } finally {
    reader.releaseLock();
  }
}