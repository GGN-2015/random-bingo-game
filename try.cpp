#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cassert>

// Stores the target number of checked cells around each grid
int aim[7][7];

// Maximum possible checked cells around each grid position
const int max_siz[7][7] = {
    {},
    {0, 4, 6, 6, 6, 4},
    {0, 6, 9, 9, 9, 6},
    {0, 6, 9, 9, 9, 6},
    {0, 6, 9, 9, 9, 6},
    {0, 4, 6, 6, 6, 4},
};

// Example target configuration (commented out)
// int aim[7][7] = {
//     {},
//     {0, 2, 0, 0, 0, 0},
//     {0, 0, 3, 0, 0, 0},
//     {0, 0, 0, 3, 0, 0},
//     {0, 0, 0, 0, 3, 0},
//     {0, 0, 0, 0, 0, 2}
// };

// Current grid configuration being evaluated
int now[7][7];
// Solution grid configuration
int sol[7][7];
// Count of valid bingo configurations found
int bingo_cnt = 0;

// File pointer for data storage
FILE *data_fp;

/**
 * Check if there is a line of five consecutive '1's
 * (horizontal, vertical, or diagonal)
 */
bool hasFiveConsecutiveOnes(int grid[7][7]) {
    // Check horizontal lines
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

    // Check vertical lines
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

    // Check main diagonal
    int count = 0;
    for (int i = 0; i < 5; ++i) {
        if (grid[i+1][i+1] == 1) {
            count++;
            if (count == 5) return true;
        } else {
            count = 0;
        }
    }

    // Check anti-diagonal
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

/**
 * Validate if the current configuration meets all conditions:
 * 1. For checked cells (1), the count of adjacent checked cells matches 'aim'
 * 2. For unchecked cells (0), the count does not match 'aim'
 */
bool correct() {
    int calc[6][6] = {};
    for(int i = 1; i <= 5; i += 1) {
        for(int j = 1; j <= 5; j += 1) {
            // Calculate adjacent checked cells
            for(int dx = -1; dx <= 1; dx += 1) {
                for(int dy = -1; dy <= 1; dy += 1) {
                    calc[i][j] += (now[i + dx][j + dy] == 1);
                }
            }
            // Validate current cell
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

/**
 * Save the current valid solution to file and memory
 */
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

/**
 * Save current bingo configuration to data file
 */
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

// Total number of configurations evaluated
int total_cnt = 0;
// Number of valid solutions found
int ans_cnt = 0;

/**
 * Depth-first search to explore all possible configurations
 * x, y: Current grid coordinates being evaluated
 */
void dfs(int x, int y) {
    // When all grids have been processed
    if(x == 6) {
        total_cnt += 1;
        // Check if it forms a bingo line
        if(hasFiveConsecutiveOnes(now)) {
            bingo_cnt += 1;
            save_bingo();
            // Validate against problem constraints
            if(correct()) {
                ans_cnt += 1;
                win();
            }
        }
        return;
    }
    
    // Calculate next grid coordinates
    int nx = x;
    int ny = y + 1;
    if(ny >= 6) {
        nx = x + 1;
        ny = 1;
    }

    // Try both possible states: 0 (unchecked) and 1 (checked)
    for(int i = 0; i < 2; i += 1) {
        now[x][y] = i;
        dfs(nx, ny);
        now[x][y] = -1; // Backtrack
    }
}

/**
 * Solve the puzzle for given target values
 * inp: 5x5 array of target values
 * disp: Whether to display solution details
 * Returns: Number of valid solutions found
 */
int get_solution(int inp[5][5], bool disp=false) {
    // Initialize counters and state
    ans_cnt = 0;
    total_cnt = 0;
    bingo_cnt = 0;
    memset(now, 0xff, sizeof(now));

    // Copy input target values
    for(int i = 0; i < 5; i += 1) {
        for(int j = 0; j < 5; j += 1) {
            aim[i + 1][j + 1] = inp[i][j];
        }
    }

    // Start DFS from top-left grid
    dfs(1, 1);

    // Display results if requested
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

/**
 * Main function: Read input, solve puzzle, and output results
 */
int main() {
    // Initialize data file
    data_fp = fopen("data.txt", "r");
    if(data_fp == nullptr) {
        data_fp = fopen("data.txt", "w"); // Create new file if not exists
    }else {
        fclose(data_fp);
        data_fp = nullptr; // File already exists
    }

    // Clear temporary answer file
    FILE* fpout = fopen("temp_ans.txt", "w");
    if(fpout != nullptr) {
        fclose(fpout);
    }
    
    // Read input target values
    int inp[5][5];
    for(int i = 1; i <= 5; i += 1) {
        for(int j = 1; j <= 5; j += 1) {
            scanf("%d", &inp[i-1][j-1]);
        }
    }

    // Solve and print the number of solutions
    int ans = get_solution(inp);
    printf("%d\n", ans);

    // Clean up resources
    if(data_fp != nullptr) {
        fclose(data_fp);
    }
    return 0;
}