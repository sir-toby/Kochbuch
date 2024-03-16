import { Component } from '@angular/core';
import { ToastService } from '../toast.service';
import { ToastType } from '../toast';

@Component({
  selector: 'app-toast',
  templateUrl: './toast.component.html',
  styleUrl: './toast.component.css'
})
export class ToastComponent {
  constructor(public toastService: ToastService) { }
  public toastType = ToastType;

  createToast(type: string): void {
    switch (type) {
      case "success":
        this.toastService.addToast(type, "this is a testmessage", this.toastType.success);
        break;
      case "warning":
        this.toastService.addToast(type, "this is a testmessage", this.toastType.warning);
        break;
      case "failure":
        this.toastService.addToast(type, "this is a testmessage", this.toastType.failure);
        break;
      case "info":
        this.toastService.addToast(type, "this is a testmessage", this.toastType.info);
        break;
    }
  }
}