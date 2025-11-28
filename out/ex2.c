#include <stdio.h>
#include "runtime.c"

int main() {
    int temperatura = 40;

    if (temperatura > 30) {
            alerta_var("Monitor", "Temperatura em ", temperatura);
            alerta_var("Celular", "Temperatura em ", temperatura);
        }
    return 0;
}