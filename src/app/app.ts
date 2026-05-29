import { Component, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';

interface Course {
  title: string;
  image: string;
  alt: string;
}

interface Testimonial {
  name: string;
  text: string;
  avatar: string;
}

interface BlogPost {
  title: string;
  excerpt: string;
  image: string;
}

@Component({
  selector: 'app-root',
  imports: [FormsModule],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected menuOpen = signal(false);

  protected newsletterEmail = '';

  protected contactForm = {
    nombre: '',
    email: '',
    mensaje: ''
  };

  protected courses: Course[] = [
    { title: 'Fundamentos del emprendimiento', image: '/images/course-1.svg', alt: 'Curso de emprendimiento' },
    { title: 'Marketing digital para startups', image: '/images/course-2.svg', alt: 'Curso de marketing digital' },
    { title: 'Liderazgo y gestión de equipos', image: '/images/course-3.svg', alt: 'Curso de liderazgo' }
  ];

  protected testimonials: Testimonial[] = [
    {
      name: 'María González',
      text: 'WonPLUS me ayudó a estructurar mi negocio desde cero. Los cursos son claros y muy prácticos.',
      avatar: '/images/avatars/avatar-1.svg'
    },
    {
      name: 'Carlos Ruiz',
      text: 'La plataforma es intuitiva y el contenido de calidad. Recomendada para todo emprendedor.',
      avatar: '/images/avatars/avatar-2.svg'
    },
    {
      name: 'Ana Torres',
      text: 'Gracias a WonPLUS lancé mi emprendimiento con confianza. El soporte es excelente.',
      avatar: '/images/avatars/avatar-3.svg'
    }
  ];

  protected blogPosts: BlogPost[] = [
    {
      title: '5 claves para iniciar tu negocio',
      excerpt: 'Consejos esenciales para dar el primer paso.',
      image: '/images/blog/blog-1.svg'
    },
    {
      title: 'Finanzas para emprendedores',
      excerpt: 'Aprende a gestionar el capital de tu startup.',
      image: '/images/blog/blog-2.svg'
    },
    {
      title: 'Liderazgo en equipos pequeños',
      excerpt: 'Cómo motivar y dirigir tu equipo con éxito.',
      image: '/images/blog/blog-3.svg'
    }
  ];

  toggleMenu(): void {
    this.menuOpen.update((open) => !open);
  }

  closeMenu(): void {
    this.menuOpen.set(false);
  }

  onNewsletterSubmit(event: Event): void {
    event.preventDefault();
    if (this.newsletterEmail.trim()) {
      alert(`¡Gracias por suscribirte con ${this.newsletterEmail}!`);
      this.newsletterEmail = '';
    }
  }

  onContactSubmit(event: Event): void {
    event.preventDefault();
    alert(`Mensaje enviado. Te contactaremos pronto, ${this.contactForm.nombre}.`);
    this.contactForm = { nombre: '', email: '', mensaje: '' };
  }
}
