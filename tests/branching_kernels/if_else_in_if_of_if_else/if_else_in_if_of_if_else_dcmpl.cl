__kernel __attribute__((reqd_work_group_size(4, 4, 4)))
void if_else_in_if_of_if_else(int x, __global int *data, int y)
{
    int var5;
    uint var8;
    var8 = get_global_id(0);
    if (1 == (int)var8) {
        var8 = get_global_id(2);
        data[get_global_id(0)] = (get_global_id(1) * x) - (ulong)y;
        if (x < y) {
            var5 = ((ulong)get_global_offset(2) + (ulong)x) + (get_global_id(2) - get_global_offset(2));
        }
        else {
            var5 = (ulong)y + get_global_id(1);
        }
    }
    else {
        var5 = get_global_id(0) * y;
    }
    data[var8] = var5;
    data[get_global_id(1)] = x;
}
