import { Injectable, signal } from '@angular/core';

export interface Product {
  id: number;
  name: string;
  price: number;
  stock: number;
}

export interface CartItem {
  productId: number;
  name: string;
  price: number;
  quantity: number;
}

export interface LastSale {
  total: number;
  items: CartItem[];
}

export interface SaleRecord extends LastSale {
  id: number;
  date: Date;
}

const LOW_STOCK_LIMIT = 5;

function atHours(base: Date, daysAgo: number, hours: number, minutes: number): Date {
  const date = new Date(base);
  date.setDate(date.getDate() - daysAgo);
  date.setHours(hours, minutes, 0, 0);
  return date;
}

@Injectable({ providedIn: 'root' })
export class ProductService {
  private nextId = 6;
  private nextSaleId = 1;

  readonly products = signal<Product[]>([
    { id: 1, name: 'Café premium', price: 18000, stock: 3 },
    { id: 2, name: 'Cuaderno emprendedor', price: 12000, stock: 14 },
    { id: 3, name: 'Kit de branding', price: 85000, stock: 2 },
    { id: 4, name: 'Camiseta WonPLUS', price: 45000, stock: 22 },
    { id: 5, name: 'Pack de stickers', price: 8000, stock: 4 },
  ]);

  readonly lastSale = signal<LastSale | null>(null);
  readonly sales = signal<SaleRecord[]>(this.createSampleSales());

  isLowStock(product: Product): boolean {
    return product.stock <= LOW_STOCK_LIMIT;
  }

  searchByName(query: string): Product[] {
    const term = query.trim().toLowerCase();
    if (!term) {
      return this.products();
    }
    return this.products().filter((product) => product.name.toLowerCase().includes(term));
  }

  addProduct(name: string, price: number, stock: number): void {
    const product: Product = {
      id: this.nextId++,
      name: name.trim(),
      price,
      stock,
    };
    this.products.update((list) => [...list, product]);
  }

  updateProduct(id: number, name: string, price: number, stock: number): void {
    this.products.update((list) =>
      list.map((product) =>
        product.id === id ? { ...product, name: name.trim(), price, stock } : product
      )
    );
  }

  decreaseStock(items: CartItem[]): boolean {
    const current = this.products();
    for (const item of items) {
      const product = current.find((entry) => entry.id === item.productId);
      if (!product || product.stock < item.quantity) {
        return false;
      }
    }

    this.products.update((list) =>
      list.map((product) => {
        const item = items.find((entry) => entry.productId === product.id);
        return item ? { ...product, stock: product.stock - item.quantity } : product;
      })
    );
    return true;
  }

  completeSale(items: CartItem[], total: number): boolean {
    if (!this.decreaseStock(items)) {
      return false;
    }
    this.lastSale.set({ items, total });
    this.sales.update((list) => [
      {
        id: this.nextSaleId++,
        date: new Date(),
        items,
        total,
      },
      ...list,
    ]);
    return true;
  }

  salesByPeriod(period: 'day' | 'week' | 'month'): SaleRecord[] {
    const start = this.periodStart(period);
    return this.sales().filter((sale) => sale.date >= start);
  }

  private periodStart(period: 'day' | 'week' | 'month'): Date {
    const start = new Date();
    start.setHours(0, 0, 0, 0);

    if (period === 'week') {
      start.setDate(start.getDate() - 6);
    }

    if (period === 'month') {
      start.setDate(start.getDate() - 29);
    }

    return start;
  }

  private createSampleSales(): SaleRecord[] {
    const now = new Date();
    const samples: Array<{ daysAgo: number; hours: number; minutes: number; items: CartItem[] }> = [
      {
        daysAgo: 0,
        hours: 9,
        minutes: 20,
        items: [{ productId: 1, name: 'Café premium', price: 18000, quantity: 2 }],
      },
      {
        daysAgo: 0,
        hours: 14,
        minutes: 5,
        items: [
          { productId: 4, name: 'Camiseta WonPLUS', price: 45000, quantity: 1 },
          { productId: 5, name: 'Pack de stickers', price: 8000, quantity: 3 },
        ],
      },
      {
        daysAgo: 2,
        hours: 11,
        minutes: 40,
        items: [{ productId: 2, name: 'Cuaderno emprendedor', price: 12000, quantity: 4 }],
      },
      {
        daysAgo: 4,
        hours: 16,
        minutes: 10,
        items: [{ productId: 3, name: 'Kit de branding', price: 85000, quantity: 1 }],
      },
      {
        daysAgo: 12,
        hours: 10,
        minutes: 30,
        items: [
          { productId: 4, name: 'Camiseta WonPLUS', price: 45000, quantity: 2 },
          { productId: 2, name: 'Cuaderno emprendedor', price: 12000, quantity: 1 },
        ],
      },
      {
        daysAgo: 18,
        hours: 13,
        minutes: 15,
        items: [{ productId: 1, name: 'Café premium', price: 18000, quantity: 3 }],
      },
    ];

    return samples
      .map((sample) => {
        const date = atHours(now, sample.daysAgo, sample.hours, sample.minutes);
        const total = sample.items.reduce((sum, item) => sum + item.price * item.quantity, 0);
        return {
          id: this.nextSaleId++,
          date,
          items: sample.items,
          total,
        };
      })
      .sort((a, b) => b.date.getTime() - a.date.getTime());
  }
}
