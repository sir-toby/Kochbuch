export interface Toast {
    title: string,
    message: string,
    type: ToastType;
}

export enum ToastType {
    success = "SUCCESS",
    warning = "WARNING",
    failure = "FAILURE",
    info = "INFO"
}
