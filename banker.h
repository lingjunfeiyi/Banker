#define MAX_PROC 10
#define MAX_RES 5

typedef struct
{
    int proc_num;
    int res_num;
    int Max[MAX_PROC][MAX_RES];
    int Allocation[MAX_PROC][MAX_RES];
    int Available[MAX_RES];
} BankerState;

// 核心函数声明
int safety_check(BankerState *state, int *safe_seq);
int request_resources(BankerState *state, int pid, int *request);