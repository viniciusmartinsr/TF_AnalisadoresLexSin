/*Implementa as 4 funções obrigatórias (PDF p.5):

ligar(id)

desligar(id)

alerta(id, msg)

alerta(id, msg, var)

Estas funções são incluídas no .c final ou compiladas separadamente.*/

// runtime.c

#include <stdio.h>

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

void alerta(char* id_device, char* msg, int var) {
    printf("%s recebeu o alerta:\n", id_device);
    printf("%s %d\n", msg, var);
}
