export interface Toast {
    title: string,
    message: string,
    type: ToastType;
}

export enum ToastType {
    'Success',
    'Warning',
    'Failure',
    'Info'
}
