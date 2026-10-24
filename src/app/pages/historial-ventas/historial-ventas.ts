import { Component, computed, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';
import * as XLSX from 'xlsx';
import { ProductService, SaleRecord } from '../../services/product.service';

type HistoryPeriod = 'day' | 'week' | 'month';

@Component({
  selector: 'app-historial-ventas',
  imports: [RouterLink],
  templateUrl: './historial-ventas.html',
  styleUrl: './historial-ventas.scss',
})
export class HistorialVentas {
  private products = inject(ProductService);

  protected period = signal<HistoryPeriod>('day');
  protected downloadNote = signal('');

  protected summaries = computed(() => [
    {
      id: 'day' as const,
      title: 'Ventas del día',
      sales: this.products.salesByPeriod('day'),
    },
    {
      id: 'week' as const,
      title: 'Ventas de la semana',
      sales: this.products.salesByPeriod('week'),
    },
    {
      id: 'month' as const,
      title: 'Ventas del mes',
      sales: this.products.salesByPeriod('month'),
    },
  ]);

  protected visibleSales = computed(() => this.products.salesByPeriod(this.period()));

  protected visibleTitle = computed(() => {
    const current = this.summaries().find((item) => item.id === this.period());
    return current?.title ?? 'Historial';
  });

  selectPeriod(period: HistoryPeriod): void {
    this.period.set(period);
    this.downloadNote.set('');
  }

  downloadExcel(): void {
    const sales = this.visibleSales();
    const rows: (string | number)[][] = [
      ['Fecha', 'Productos', 'Total (COP)'],
      ...sales.map((sale) => [this.formatDate(sale.date), this.itemsLabel(sale), sale.total]),
      [],
      ['Cantidad de ventas', sales.length],
      ['Suma del periodo', this.totalOf(sales)],
    ];
    const sheet = XLSX.utils.aoa_to_sheet(rows);
    const book = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(book, sheet, 'Ventas');
    const periodName =
      this.period() === 'day' ? 'dia' : this.period() === 'week' ? 'semana' : 'mes';
    const fileName = `wonplus-ventas-${periodName}.xlsx`;
    XLSX.writeFile(book, fileName);
    this.downloadNote.set(`Se descargó ${fileName}`);
  }

  totalOf(sales: SaleRecord[]): number {
    return sales.reduce((sum, sale) => sum + sale.total, 0);
  }

  itemsLabel(sale: SaleRecord): string {
    return sale.items.map((item) => `${item.quantity} × ${item.name}`).join(', ');
  }

  formatMoney(value: number): string {
    return new Intl.NumberFormat('es-CO', {
      style: 'currency',
      currency: 'COP',
      maximumFractionDigits: 0,
    }).format(value);
  }

  formatDate(date: Date): string {
    return new Intl.DateTimeFormat('es-CO', {
      dateStyle: 'medium',
      timeStyle: 'short',
    }).format(date);
  }
}
