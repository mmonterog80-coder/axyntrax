#include <iostream>

unsigned long long factorial(int n) {
    if (n < 0) return 0;
    unsigned long long result = 1;
    for (int i = 1; i <= n; ++i) {
        result *= i;
    }
    return result;
}

int main() {
    int num;
    std::cout << "Ingrese un numero: ";
    std::cin >> num;
    std::cout << "El factorial de " << num << " es: " << factorial(num) << std::endl;
    return 0;
}