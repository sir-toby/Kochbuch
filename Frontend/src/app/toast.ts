export interface Toast {
    title: string,
    message: string,
    type: ToastType;
}

export enum ToastType {
    'success',
    'warning',
    'failure',
    'info'
}
