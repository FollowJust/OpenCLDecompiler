__kernel __attribute__((reqd_work_group_size(4, 4, 4)))
void if_else_and_if_else_0_labels(int x, __global int *data, int y)
{
    uint var2;
    uint var3;
    int var5;
    uint var6;
    var3 = get_global_id(0);
    if (1 != var3) {
        var5 = get_global_id(0) * y;
        var2 = get_global_id(1);
    }
    else {
        var2 = get_global_id(1);
        var3 = 1;
        var5 = (get_global_id(1) * x) - (uint)y;
    }
    var6 = x < y ? (ulong)x + get_global_id(2) : (ulong)y + var2;
    data[var3] = var5;
    data[get_global_id(2)] = var6;
    data[var2] = x;
}
