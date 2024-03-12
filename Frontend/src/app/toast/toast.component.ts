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
  private toastType = ToastType;

  createToast(): void {
    this.toastService.addToast("Test", "this is a testmessage", this.toastType.Success)

  }
}