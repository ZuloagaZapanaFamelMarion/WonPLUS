import { Component, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { EventLogService } from '../../services/event-log.service';

@Component({
  selector: 'app-login',
  imports: [FormsModule, RouterLink],
  templateUrl: './login.html',
  styleUrl: './login.scss',
})
export class Login {
  private events = inject(EventLogService);

  protected loginForm = {
    email: '',
    password: '',
  };
  protected loginErrors: { email?: string; password?: string } = {};
  protected lastEvent = signal('');
  protected accepted = signal(false);

  validateLoginForm(): boolean {
    this.loginErrors = {};
    let valid = true;

    if (!this.loginForm.email.trim()) {
      this.loginErrors.email = 'El correo es obligatorio';
      valid = false;
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(this.loginForm.email)) {
      this.loginErrors.email = 'Ingresa un correo válido';
      valid = false;
    }

    if (!this.loginForm.password.trim()) {
      this.loginErrors.password = 'La contraseña es obligatoria';
      valid = false;
    } else if (this.loginForm.password.length < 6) {
      this.loginErrors.password = 'La contraseña debe tener al menos 6 caracteres';
      valid = false;
    }

    return valid;
  }

  onLoginSubmit(event: Event): void {
    event.preventDefault();
    this.accepted.set(false);

    if (!this.validateLoginForm()) {
      const reason = this.loginErrors.email ?? this.loginErrors.password ?? 'datos inválidos';
      this.lastEvent.set(this.events.record('LOGIN', `rechazo: ${reason}`).text);
      return;
    }

    this.lastEvent.set(this.events.record('LOGIN', 'resultado: ingreso aceptado').text);
    this.accepted.set(true);
  }
}
