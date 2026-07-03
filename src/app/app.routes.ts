import { Routes } from '@angular/router';
import { Home } from './pages/home/home';
import { NewsletterSuccess } from './pages/newsletter-success/newsletter-success';
import { BlogPost1 } from './pages/blog/blog-post-1/blog-post-1';
import { BlogPost2 } from './pages/blog/blog-post-2/blog-post-2';
import { BlogPost3 } from './pages/blog/blog-post-3/blog-post-3';
import { FundamentosEmprendimiento } from './pages/cursos/fundamentos-emprendimiento/fundamentos-emprendimiento';
import { MarketingDigital } from './pages/cursos/marketing-digital/marketing-digital';
import { LiderazgoEquipos } from './pages/cursos/liderazgo-equipos/liderazgo-equipos';

export const routes: Routes = [
  { path: '', component: Home },
  { path: 'newsletter-success', component: NewsletterSuccess },
  { path: 'blog/5-claves-iniciar-negocio', component: BlogPost1 },
  { path: 'blog/finanzas-emprendedores', component: BlogPost2 },
  { path: 'blog/liderazgo-equipos-pequenos', component: BlogPost3 },
  { path: 'cursos/fundamentos-emprendimiento', component: FundamentosEmprendimiento },
  { path: 'cursos/marketing-digital', component: MarketingDigital },
  { path: 'cursos/liderazgo-equipos', component: LiderazgoEquipos },
];
