import { Component, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { Product, ProductService } from '../../services/product.service';

@Component({
  selector: 'app-gestion-productos',
  imports: [FormsModule, RouterLink],
  templateUrl: './gestion-productos.html',
  styleUrl: './gestion-productos.scss',
})
export class GestionProductos {
  private products = inject(ProductService);

  protected catalog = this.products.products;
  protected editingId: number | null = null;
  protected formError = '';
  protected form = {
    name: '',
    price: '',
    stock: '',
  };

  isLowStock(product: Product): boolean {
    return this.products.isLowStock(product);
  }

  formatMoney(value: number): string {
    return new Intl.NumberFormat('es-CO', {
      style: 'currency',
      currency: 'COP',
      maximumFractionDigits: 0,
    }).format(value);
  }

  startEdit(product: Product): void {
    this.editingId = product.id;
    this.form = {
      name: product.name,
      price: String(product.price),
      stock: String(product.stock),
    };
    this.formError = '';
  }

  cancelEdit(): void {
    this.editingId = null;
    this.form = { name: '', price: '', stock: '' };
    this.formError = '';
  }

  saveProduct(event: Event): void {
    event.preventDefault();
    const name = this.form.name.trim();
    const price = Number(this.form.price);
    const stock = Number(this.form.stock);

    if (!name) {
      this.formError = 'El nombre es obligatorio.';
      return;
    }
    if (!Number.isFinite(price) || price < 0) {
      this.formError = 'Ingresa un precio válido.';
      return;
    }
    if (!Number.isInteger(stock) || stock < 0) {
      this.formError = 'Ingresa un stock válido.';
      return;
    }

    if (this.editingId === null) {
      this.products.addProduct(name, price, stock);
    } else {
      this.products.updateProduct(this.editingId, name, price, stock);
    }

    this.cancelEdit();
  }
}
