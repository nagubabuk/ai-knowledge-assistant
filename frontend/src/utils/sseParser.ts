import type { SSEEvent } from "../types/chat";

export class SSEParser {
  private buffer = "";

  private eventType = "message";

  private eventData: string[] = [];

  private eventId?: string;

  feed(chunk: string): SSEEvent[] {
    this.buffer += chunk;

    const events: SSEEvent[] = [];

    while (true) {
      const lineEnd = this.findLineEnd();

      if (lineEnd === -1) {
        break;
      }

      const { line, consumed } = lineEnd;

      this.buffer = this.buffer.slice(consumed);

      if (line === "") {
        const event = this.dispatchEvent();

        if (event) {
          events.push(event);
        }

        continue;
      }

      this.processLine(line);
    }

    return events;
  }

  end(): SSEEvent[] {
    const events: SSEEvent[] = [];

    if (this.buffer.length > 0) {
      this.processLine(this.buffer);
      this.buffer = "";
    }

    const event = this.dispatchEvent();

    if (event) {
      events.push(event);
    }

    return events;
  }

  private findLineEnd():
    | { line: string; consumed: number }
    | -1 {
    for (let index = 0; index < this.buffer.length; index++) {
      const character = this.buffer[index];

      if (character === "\n") {
        return {
          line: this.buffer.slice(0, index),
          consumed: index + 1,
        };
      }

      if (character === "\r") {
        if (
          index + 1 < this.buffer.length &&
          this.buffer[index + 1] === "\n"
        ) {
          return {
            line: this.buffer.slice(0, index),
            consumed: index + 2,
          };
        }

        return {
          line: this.buffer.slice(0, index),
          consumed: index + 1,
        };
      }
    }

    return -1;
  }

  private processLine(line: string): void {
    // SSE comments start with ":" and should be ignored.
    if (line.startsWith(":")) {
      return;
    }

    const separatorIndex = line.indexOf(":");

    if (separatorIndex === -1) {
      return;
    }

    const field = line.slice(0, separatorIndex);

    let value = line.slice(separatorIndex + 1);

    // SSE allows an optional space after the colon.
    if (value.startsWith(" ")) {
      value = value.slice(1);
    }

    switch (field) {
      case "event":
        this.eventType = value || "message";
        break;

      case "data":
        this.eventData.push(value);
        break;

      case "id":
        this.eventId = value;
        break;

      case "retry":
        // We are not implementing automatic retry yet.
        break;

      default:
        break;
    }
  }

  private dispatchEvent(): SSEEvent | null {
    if (this.eventData.length === 0) {
      this.resetEvent();
      return null;
    }

    const event: SSEEvent = {
      event: this.eventType,
      data: this.eventData.join("\n"),
    };

    if (this.eventId !== undefined) {
      event.id = this.eventId;
    }

    this.resetEvent();

    return event;
  }

  private resetEvent(): void {
    this.eventType = "message";
    this.eventData = [];
    this.eventId = undefined;
  }
}