#include "banker.h"

int request_resources(BankerState *state, int pid, int *request)
{
    // 步骤1：检查请求是否合法
    for (int i = 0; i < state->res_num; i++)
    {
        if (request[i] > state->Max[pid][i] - state->Allocation[pid][i] ||
            request[i] > state->Available[i])
        {
            return -1; // 非法请求
        }
    }

    // 模拟分配
    for (int i = 0; i < state->res_num; i++)
    {
        state->Available[i] -= request[i];
        state->Allocation[pid][i] += request[i];
    }

    // 检查安全性
    int safe_seq[MAX_PROC];
    int is_safe = safety_check(state, safe_seq);

    if (!is_safe)
    { // 回滚操作
        for (int i = 0; i < state->res_num; i++)
        {
            state->Available[i] += request[i];
            state->Allocation[pid][i] -= request[i];
        }
        return 0;
    }
    return 1;
}