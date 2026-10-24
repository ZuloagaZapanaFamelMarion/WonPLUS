import { Component, inject } from '@angular/core';
import { RouterLink } from '@angular/router';
import { ProductService } from '../../services/product.service';

@Component({
  selector: 'app-venta-cobrada',
  imports: [RouterLink],
  templateUrl: './venta-cobrada.html',
  styleUrl: './venta-cobrada.scss',
})
export class VentaCobrada {
  private products = inject(ProductService);
  protected sale = this.products.lastSale;

  formatMoney(value: number): string {
    return new Intl.NumberFormat('es-CO', {
      style: 'currency',
      currency: 'COP',
      maximumFractionDigits: 0,
    }).format(value);
  }
}
