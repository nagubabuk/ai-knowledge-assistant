export type SSEEventType =
  | "message"
  | "done"
  | "error";

export interface SSEEvent {
  event: SSEEventType | string;
  data: string;
  id?: string;
}