#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cassert>

int aim[7][7];

const int max_siz[7][7] = {
    {},
    {0, 4, 6, 6, 6, 4},
    {0, 6, 9, 9, 9, 6},
    {0, 6, 9, 9, 9, 6},
    {0, 6, 9, 9, 9, 6},
    {0, 4, 6, 6, 6, 4},
};

// int aim[7][7] = {
//     {},
//     {0, 2, 0, 0, 0, 0},
//     {0, 0, 3, 0, 0, 0},
//     {0, 0, 0, 3, 0, 0},
//     {0, 0, 0, 0, 3, 0},
//     {0, 0, 0, 0, 0, 2}
// };

int now[7][7];
int sol[7][7];
int bingo_cnt = 0;

FILE *data_fp;

bool hasFiveConsecutiveOnes(int grid[7][7]) {
    // 检查横向连续的1
    for (int i = 0; i < 5; ++i) {
        int count = 0;
        for (int j = 0; j < 5; ++j) {
            if (grid[i+1][j+1] == 1) {
                count++;
                if (count == 5) return true;
            } else {
                count = 0;
            }
        }
    }

    // 检查纵向连续的1
    for (int j = 0; j < 5; ++j) {
        int count = 0;
        for (int i = 0; i < 5; ++i) {
            if (grid[i+1][j+1] == 1) {
                count++;
                if (count == 5) return true;
            } else {
                count = 0;
            }
        }
    }

    // 检查主对角线
    int count = 0;
    for (int i = 0; i < 5; ++i) {
        if (grid[i+1][i+1] == 1) {
            count++;
            if (count == 5) return true;
        } else {
            count = 0;
        }
    }

    // 检查副对角线
    count = 0;
    for (int i = 0; i < 5; ++i) {
        if (grid[i+1][5 - i] == 1) {
            count++;
            if (count == 5) return true;
        } else {
            count = 0;
        }
    }

    return false;
}

bool correct() {
    int calc[6][6] = {};
    for(int i = 1; i <= 5; i += 1) {
        for(int j = 1; j <= 5; j += 1) {
            for(int dx = -1; dx <= 1; dx += 1) {
                for(int dy = -1; dy <= 1; dy += 1) {
                    calc[i][j] += (now[i + dx][j + dy] == 1);
                }
            }
            if(now[i][j] == 1 && calc[i][j] != aim[i][j]) {
                return false;
            }
            if(now[i][j] == 0 && calc[i][j] == aim[i][j]) {
                return false;
            }
        }
    }
    return true;
}

void win() {
    memcpy(sol, now, sizeof(now));
    FILE* fpout = fopen("temp_ans.txt", "a");
    for(int i = 1; i <= 5; i += 1) {
        for(int j = 1; j <= 5; j += 1) {
            fprintf(fpout, "%d ", sol[i][j]);
        }
        fprintf(fpout, "\n");
    }
    fclose(fpout);
}

void save_bingo() {
    if(data_fp != nullptr) {
        fprintf(data_fp, "==========\n");
        for(int i = 1; i <= 5; i += 1) {
            for(int j = 1; j <= 5; j += 1) {
                fprintf(data_fp, "%d ", now[i][j]);
            }
            fprintf(data_fp, "\n");
        }
    }
}

int total_cnt = 0;
int ans_cnt = 0;
void dfs(int x, int y) {
    if(x == 6) {
        total_cnt += 1;
        if(hasFiveConsecutiveOnes(now)) {
            bingo_cnt += 1;
            save_bingo();
            if(correct()) {
                ans_cnt += 1;
                win();
            }
        }
        return;
    }
    int nx = x; // solve next
    int ny = y + 1;
    if(ny >= 6) {
        nx = x + 1;
        ny = 1;
    }

    for(int i = 0; i < 2; i += 1) {
        now[x][y] = i;
        dfs(nx, ny);
        now[x][y] = -1;
    }
}

int get_solution(int inp[5][5], bool disp=false) {
    ans_cnt = 0;
    total_cnt = 0;
    bingo_cnt = 0;
    memset(now, 0xff, sizeof(now));

    for(int i = 0; i < 5; i += 1) {
        for(int j = 0; j < 5; j += 1) {
            aim[i + 1][j + 1] = inp[i][j];
        }
    }

    dfs(1, 1);

    if(disp) {
        printf("ans_cnt = %d \n", ans_cnt);
        printf("cnt = %d / 33554432\n", total_cnt);
        printf("bingo_cnt = %d / 9717109\n", bingo_cnt);
        printf("==========\n");
    
        if(ans_cnt == 1) {
            for(int i = 1; i <= 5; i += 1) {
                for(int j = 1; j <= 5; j += 1) {
                    printf("%d ", sol[i][j]);
                }
                printf("\n");
            }
        }
    }
    return ans_cnt;
}

int main() {
    data_fp = fopen("data.txt", "r");
    if(data_fp == nullptr) {
        data_fp = fopen("data.txt", "w"); // 文件不存在需要创建
    }else {
        fclose(data_fp);
        data_fp = nullptr; // 文件已经存在
    }

    FILE* fpout = fopen("temp_ans.txt", "w");
    if(fpout != nullptr) {
        fclose(fpout);
    }
    
    int inp[5][5];
    for(int i = 1; i <= 5; i += 1) {
        for(int j = 1; j <= 5; j += 1) {
            scanf("%d", &inp[i-1][j-1]);
        }
    }

    int ans = get_solution(inp);
    printf("%d\n", ans);

    if(data_fp != nullptr) {
        fclose(data_fp);
    }
    return 0;
}
