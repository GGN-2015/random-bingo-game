#include "Checker.h"
#include <cstdio>

int main() {
    int aim[5][5] = {
        {2, 2, 3, 1, 3},
        {4, 5, 2, 4, 3},
        {2, 2, 5, 4, 3},
        {1, 5, 5, 5, 2},
        {2, 3, 4, 2, 1}
    };

    Checker checker(aim);
    printf("ans_cnt = %d\n", checker.get_ans_cnt());
    printf("touch_cnt = %d\n", checker.get_touch_cnt());
    printf("bingo_cnt = %d\n", checker.get_bingo_cnt());

    if(checker.get_ans_cnt() == 1) {
        for(int i = 0; i < 5; i += 1) {
            for(int j = 0; j < 5; j += 1) {
                printf("%d ", checker.get_solution(i, j));
            }
            printf("\n");
        }   
    }
    return 0;
}