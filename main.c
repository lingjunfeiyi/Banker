#include <stdio.h>
#include <stdlib.h>
#include "banker.h"

// 输出安全序列的函数
void print_result(int result, int *seq, int proc_num)
{
    if (result)
    {
        printf("1"); // 表示安全
        for (int i = 0; i < proc_num; i++)
        {
            printf(" %d", seq[i]);
        }
        printf("\n");
    }
    else
    {
        printf("0\n"); // 表示不安全
    }
}

int main()
{
    BankerState state;

    // 读取输入数据
    scanf("%d", &state.proc_num);
    scanf("%d", &state.res_num);

    for (int i = 0; i < state.proc_num; i++)
    {
        for (int j = 0; j < state.res_num; j++)
        {
            scanf("%d", &state.Max[i][j]);
        }
    }

    for (int i = 0; i < state.proc_num; i++)
    {
        for (int j = 0; j < state.res_num; j++)
        {
            scanf("%d", &state.Allocation[i][j]);
        }
    }

    for (int i = 0; i < state.res_num; i++)
    {
        scanf("%d", &state.Available[i]);
    }

    // 执行安全检测
    int safe_seq[MAX_PROC];
    int is_safe = safety_check(&state, safe_seq);
    print_result(is_safe, safe_seq, state.proc_num);

    return 0;
}