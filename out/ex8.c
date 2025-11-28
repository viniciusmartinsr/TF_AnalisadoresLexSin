#include <stdio.h>
#include "runtime.c"

int main() {
    int temperatura = 0;

    alerta_var("Termometro", "Temperatura esta em", temperatura);
    return 0;
}