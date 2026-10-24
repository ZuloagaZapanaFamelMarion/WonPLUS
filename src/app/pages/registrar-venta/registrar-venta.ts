import { Component, computed, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { EventLogService } from '../../services/event-log.service';
import { CartItem, ProductService } from '../../services/product.service';

@Component({
  selector: 'app-registrar-venta',
  imports: [FormsModule, RouterLink],
  templateUrl: './registrar-venta.html',
  styleUrl: './registrar-venta.scss',
})
export class RegistrarVenta {
  private products = inject(ProductService);
  private events = inject(EventLogService);
  private router = inject(Router);

  protected search = signal('');
  protected cart = signal<CartItem[]>([]);
  protected chargeError = '';

  protected results = computed(() => this.products.searchByName(this.search()));
  protected total = computed(() =>
    this.cart().reduce((sum, item) => sum + item.price * item.quantity, 0)
  );

  get searchValue(): string {
    return this.search();
  }

  set searchValue(value: string) {
    this.search.set(value);
  }

  formatMoney(value: number): string {
    return new Intl.NumberFormat('es-CO', {
      style: 'currency',
      currency: 'COP',
      maximumFractionDigits: 0,
    }).format(value);
  }

  addToCart(productId: number): void {
    const product = this.products.products().find((item) => item.id === productId);
    if (!product || product.stock <= 0) {
      return;
    }

    this.chargeError = '';
    this.cart.update((items) => {
      const existing = items.find((item) => item.productId === productId);
      if (existing) {
        if (existing.quantity >= product.stock) {
          return items;
        }
        return items.map((item) =>
          item.productId === productId ? { ...item, quantity: item.quantity + 1 } : item
        );
      }

      return [
        ...items,
        {
          productId: product.id,
          name: product.name,
          price: product.price,
          quantity: 1,
        },
      ];
    });
  }

  removeFromCart(productId: number): void {
    this.cart.update((items) => items.filter((item) => item.productId !== productId));
  }

  decreaseQuantity(productId: number): void {
    this.cart.update((items) =>
      items
        .map((item) =>
          item.productId === productId ? { ...item, quantity: item.quantity - 1 } : item
        )
        .filter((item) => item.quantity > 0)
    );
  }

  charge(): void {
    const items = this.cart();
    if (!items.length) {
      this.chargeError = 'Agrega al menos un producto para cobrar.';
      return;
    }

    const ok = this.products.completeSale(items, this.total());
    if (!ok) {
      this.chargeError = 'No hay stock suficiente para completar la venta.';
      this.events.record('VENTAS', 'rechazo: stock insuficiente');
      return;
    }

    this.events.record('VENTAS', `venta cobrada por ${this.total()}`);
    this.router.navigate(['/venta-cobrada']);
  }
}
