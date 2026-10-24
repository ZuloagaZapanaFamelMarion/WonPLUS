import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';

interface DashboardCard {
  title: string;
  value: string;
  detail: string;
  icon: 'sales' | 'stock' | 'profit';
}

@Component({
  selector: 'app-dashboard',
  imports: [RouterLink],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.scss',
})
export class Dashboard {
  protected cards: DashboardCard[] = [
    {
      title: 'Ventas de Hoy',
      value: '$1.250.000',
      detail: '18 ventas registradas',
      icon: 'sales',
    },
    {
      title: 'Productos con Stock Bajo',
      value: '5',
      detail: 'Requieren reposición',
      icon: 'stock',
    },
    {
      title: 'Ganancia del Día',
      value: '$430.000',
      detail: 'Margen del 34%',
      icon: 'profit',
    },
  ];
}
