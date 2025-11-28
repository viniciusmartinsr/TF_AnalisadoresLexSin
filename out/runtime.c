// runtime.c

#include <stdio.h>

#define True 1
#define False 0

void ligar(char* id_device) {
    printf("%s ligado!\n", id_device);
}

void desligar(char* id_device) {
    printf("%s desligado!\n", id_device);
}

void alerta(char* id_device, char* msg) {
    printf("%s recebeu o alerta:\n", id_device);
    printf("%s\n", msg);
}

void alerta_var(char* id_device, char* msg, int var) {
    printf("%s recebeu o alerta:\n", id_device);
    printf("%s %d\n", msg, var);
}
