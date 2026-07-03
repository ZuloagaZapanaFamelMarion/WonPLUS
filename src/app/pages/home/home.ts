import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';

interface Course {
  title: string;
  image: string;
  alt: string;
  route: string;
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
  route: string;
}

@Component({
  selector: 'app-home',
  imports: [FormsModule, RouterLink],
  templateUrl: './home.html',
  styleUrl: './home.scss',
})
export class Home {
  protected newsletterEmail = '';
  protected newsletterSubmitted = false;
  protected expandedTestimonial: string | null = null;

  protected contactForm = {
    nombre: '',
    email: '',
    mensaje: '',
  };
  protected contactSubmitted = false;
  protected contactErrors: { nombre?: string; email?: string; mensaje?: string } = {};

  protected courses: Course[] = [
    { title: 'Fundamentos del emprendimiento', image: '/images/course-1.svg', alt: 'Curso de emprendimiento', route: '/cursos/fundamentos-emprendimiento' },
    { title: 'Marketing digital para startups', image: '/images/course-2.svg', alt: 'Curso de marketing digital', route: '/cursos/marketing-digital' },
    { title: 'Liderazgo y gestión de equipos', image: '/images/course-3.svg', alt: 'Curso de liderazgo', route: '/cursos/liderazgo-equipos' },
  ];

  protected testimonials: Testimonial[] = [
    {
      name: 'María González',
      text: 'WonPLUS me ayudó a estructurar mi negocio desde cero. Los cursos son claros y muy prácticos.',
      avatar: '/images/avatars/avatar-1.svg',
    },
    {
      name: 'Carlos Ruiz',
      text: 'La plataforma es intuitiva y el contenido de calidad. Recomendada para todo emprendedor.',
      avatar: '/images/avatars/avatar-2.svg',
    },
    {
      name: 'Ana Torres',
      text: 'Gracias a WonPLUS lancé mi emprendimiento con confianza. El soporte es excelente.',
      avatar: '/images/avatars/avatar-3.svg',
    },
  ];

  protected blogPosts: BlogPost[] = [
    {
      title: '5 claves para iniciar tu negocio',
      excerpt: 'Consejos esenciales para dar el primer paso.',
      image: '/images/blog/blog-1.svg',
      route: '/blog/5-claves-iniciar-negocio',
    },
    {
      title: 'Finanzas para emprendedores',
      excerpt: 'Aprende a gestionar el capital de tu startup.',
      image: '/images/blog/blog-2.svg',
      route: '/blog/finanzas-emprendedores',
    },
    {
      title: 'Liderazgo en equipos pequeños',
      excerpt: 'Cómo motivar y dirigir tu equipo con éxito.',
      image: '/images/blog/blog-3.svg',
      route: '/blog/liderazgo-equipos-pequenos',
    },
  ];

  toggleTestimonial(name: string): void {
    this.expandedTestimonial = this.expandedTestimonial === name ? null : name;
  }

  onNewsletterSubmit(event: Event): void {
    event.preventDefault();
    if (this.newsletterEmail.trim()) {
      this.newsletterSubmitted = true;
    }
  }

  validateContactForm(): boolean {
    this.contactErrors = {};
    let valid = true;

    if (!this.contactForm.nombre.trim()) {
      this.contactErrors.nombre = 'El nombre es obligatorio';
      valid = false;
    }

    if (!this.contactForm.email.trim()) {
      this.contactErrors.email = 'El correo es obligatorio';
      valid = false;
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(this.contactForm.email)) {
      this.contactErrors.email = 'Ingresa un correo válido';
      valid = false;
    }

    if (!this.contactForm.mensaje.trim()) {
      this.contactErrors.mensaje = 'El mensaje es obligatorio';
      valid = false;
    }

    return valid;
  }

  get isContactFormValid(): boolean {
    return (
      this.contactForm.nombre.trim() !== '' &&
      /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(this.contactForm.email) &&
      this.contactForm.mensaje.trim() !== ''
    );
  }

  onContactSubmit(event: Event): void {
    event.preventDefault();
    if (this.validateContactForm()) {
      this.contactSubmitted = true;
    }
  }
}
