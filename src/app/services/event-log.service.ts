import { Injectable, signal } from '@angular/core';

export interface EventLogLine {
  at: string;
  module: string;
  result: string;
  text: string;
}

@Injectable({ providedIn: 'root' })
export class EventLogService {
  readonly lines = signal<EventLogLine[]>([]);

  record(module: string, result: string): EventLogLine {
    const at = new Intl.DateTimeFormat('es-CO', {
      dateStyle: 'short',
      timeStyle: 'medium',
    }).format(new Date());
    const line: EventLogLine = {
      at,
      module,
      result,
      text: `${at} | ${module} | ${result}`,
    };
    this.lines.update((current) => [line, ...current].slice(0, 8));
    return line;
  }
}
