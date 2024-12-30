#include <stdint.h>

int main() {
    /* Comentário de 
    várias 
    linhas
    */
   int x = 0;
   int y = 1;
   // Somatório:
   int sum;

/*
Sum é igual a x + y
*/
   sum = x + y;
// Printamos o somatório
   printf("%d\n", sum);
}


/*
Errado: \/\*.*?\*\/|\/\/.*

Correto: \/\*[^*]*\*+(?:[^/*][^*]*\*+)*\/|\/\/[^\n]*

*/