#pragma once
#include <cstring>
#include <cassert>
#include <cstdio>

class Checker {
private:
    int aim[7][7];
    int now[7][7];
    int sol[7][7];
    int ans_cnt;
    int touch_cnt;
    int bingo_cnt;

    bool hasFiveConsecutiveOnes() const {
        // 检查横向连续的1
        for (int i = 0; i < 5; ++i) {
            int count = 0;
            for (int j = 0; j < 5; ++j) {
                if (now[i+1][j+1] == 1) {
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
                if (now[i+1][j+1] == 1) {
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
            if (now[i+1][i+1] == 1) {
                count++;
                if (count == 5) return true;
            } else {
                count = 0;
            }
        }

        // 检查副对角线
        count = 0;
        for (int i = 0; i < 5; ++i) {
            if (now[i+1][5 - i] == 1) {
                count++;
                if (count == 5) return true;
            } else {
                count = 0;
            }
        }

        return false;
    }
    
    bool correct() const {
        int calc[6][6] = {};
        for(int i = 1; i <= 5; i += 1) {
            for(int j = 1; j <= 5; j += 1) {
                for(int dx = -1; dx <= 1; dx += 1) {
                    for(int dy = -1; dy <= 1; dy += 1) {
                        calc[i][j] += now[i + dx][j + dy];
                    }
                }
                if(now[i][j] && calc[i][j] != aim[i][j]) {
                    return false;
                }
                if(!now[i][j] && calc[i][j] == aim[i][j]) {
                    return false;
                }
            }
        }
        return true;
    }

    bool can_cut_branch() const {
        int calc[7][7] = {};
        for(int i = 1; i <= 5; i += 1) {
            for(int j = 1; j <= 5; j += 1) {
                for(int dx = -1; dx <= 1; dx += 1) {
                    for(int dy = -1; dy <= 1; dy += 1) {
                        calc[i][j] += now[i + dx][j + dy];
                    }
                }
                if(now[i][j] && calc[i][j] > aim[i][j]) {
                    return true;
                }
            }
        }
        return false;
    }

    void debug_output() const {
        printf("==========\n");
        for(int i = 1; i <= 5; i += 1) {
            for(int j = 1; j <= 5; j += 1) {
                printf("%d ", now[i][j]);
            }
            printf("\n");
        }
    }

    void dfs(int x, int y) {
        if(x >= 6) {
            touch_cnt += 1;
            if(hasFiveConsecutiveOnes()) {
                bingo_cnt += 1;
                if(correct()) {
                    ans_cnt += 1;
                    memcpy(sol, now, sizeof(sol));
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
        //if(can_cut_branch()) return;

        for(int i = 0; i < 2; i += 1) {
            now[x][y] = i;
            dfs(nx, ny); // next x, next y
            now[x][y] = 0;
        }
    }

public:
    Checker(int arr[5][5]) :ans_cnt(0), touch_cnt(0), bingo_cnt(0) {
        memset(aim, 0x00, sizeof(aim));
        static const int max_siz[5][5] = {
            {4, 6, 6, 6, 4},
            {6, 9, 9, 9, 6},
            {6, 9, 9, 9, 6},
            {6, 9, 9, 9, 6},
            {4, 6, 6, 6, 4},
        };

        for(int i = 0; i < 5; i += 1) { // copy data
            for(int j = 0; j < 5; j += 1) {
                aim[i + 1][j + 1] = arr[i][j];
                assert(0 <= arr[i][j] && arr[i][j] <= max_siz[i][j]);
            }
        }

        ans_cnt = 0;
        dfs(1, 1);
    }

    int get_ans_cnt() const {
        return ans_cnt;
    }

    int get_touch_cnt() const {
        return touch_cnt;
    }

    int get_bingo_cnt() const {
        return bingo_cnt;
    }

    int get_solution(int i, int j) const {
        assert(0 <= i && i < 5);
        assert(0 <= j && j < 5);
        assert(ans_cnt >= 1);
        return sol[i][j];
    }
};