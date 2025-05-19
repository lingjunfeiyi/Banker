#include "banker.h"
#include <string.h>

int safety_check(BankerState *state, int *safe_seq)
{
    int work[MAX_RES];
    int finish[MAX_PROC] = {0};
    int count = 0;

    // 复制可用资源
    memcpy(work, state->Available, sizeof(work));

    while (count < state->proc_num)
    {
        int found = 0;
        for (int i = 0; i < state->proc_num; i++)
        {
            if (!finish[i])
            {
                int can_alloc = 1;
                for (int j = 0; j < state->res_num; j++)
                {
                    if (state->Max[i][j] - state->Allocation[i][j] > work[j])
                    {
                        can_alloc = 0;
                        break;
                    }
                }

                if (can_alloc)
                {
                    for (int j = 0; j < state->res_num; j++)
                        work[j] += state->Allocation[i][j];
                    safe_seq[count++] = i;
                    finish[i] = 1;
                    found = 1;
                }
            }
        }
        if (!found)
            break;
    }

    return (count == state->proc_num) ? 1 : 0;
}