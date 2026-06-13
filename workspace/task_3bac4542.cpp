#include <iostream>

int factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}

int main() {
    int numero;
    std::cout << "Ingrese un numero: ";
    std::cin >> numero;
    std::cout << "El factorial de " << numero << " es: " << factorial(numero) << std::endl;
    return 0;
}