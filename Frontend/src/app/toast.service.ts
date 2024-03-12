import { Injectable } from '@angular/core';
import { Toast, ToastType } from './toast';

@Injectable({
  providedIn: 'root'
})
export class ToastService {
  toasts: Toast[] = []

  addToast(title: string, message: string, type: ToastType): void {
    this.toasts.push({
      title: title,
      message: message,
      type: type
    })
  }

  clearAll(): void {
    this.toasts = [];
  }
}
