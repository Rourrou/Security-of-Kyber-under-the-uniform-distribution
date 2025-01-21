#include <math.h>
#include <stdio.h>

int pow2[] = {2, 4, 8, 16, 32, 64, 128, 256, 512, 1024};

int find_k(int x) {
  for (int i = 0; i < 50; i++) {
    if (x <= pow(2, i))
      return i;
  }
  return -1;
}

int main() {
  // for [-2,2]
  int res, k;
  printf("[-2,2], sample counts, need bits: average bit\n");
  for (int i = 1; i < 10; i++) {
    res = pow(5, i);
    k = find_k(res);
    printf("%d, %d: %f \n", i, k, ceil(k / (res / pow(2, k))) / i);
  }

  // for [-3,3]
  printf("\n\n");
  printf("[-3,3]\n");
  for (int i = 1; i < 10; i++) {
    res = pow(7, i);
    k = find_k(res);
    printf("%d: %f \n", i, ceil(k / (res / pow(2, k))) / i);
  }

  // for [-4,4]
  printf("\n\n");
  printf("[-4,4]\n");
  for (int i = 1; i < 10; i++) {
    res = pow(9, i);
    k = find_k(res);
    printf("%d, %d: %f \n", i, k, ceil(k / (res / pow(2, k))) / i);
  }

  return 0;
}
