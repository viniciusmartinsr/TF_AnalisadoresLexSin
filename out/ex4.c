#include <stdio.h>
#include "runtime.c"

int main() {
    int umidade = 0;

    if (umidade < 40) {
            alerta("Monitor", "Ar seco     detectado");
        }
    return 0;
}