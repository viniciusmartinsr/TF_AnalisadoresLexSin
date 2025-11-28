#include <stdio.h>
#include "runtime.c"

int main() {
    int potencia = 100;
    int movimento = 0;
    int umidade = 0;

    if (umidade < 40) {
            alerta("Monitor", "Ar seco     detectado");
        }
    if (movimento == True) {
            ligar("Lampada");
        } else {
            desligar("Lampada");
        }
    return 0;
}