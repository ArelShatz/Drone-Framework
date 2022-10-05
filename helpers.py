def insort_left_key(a, x, lo=0, hi=None, key=lambda v: v):
    element = key(x)
    if lo < 0:
        raise ValueError('lo must be non-negative')
    if hi is None:
        hi = len(a)
    while lo < hi:
        mid = (lo+hi)//2
        if key(a[mid]) < element: lo = mid+1
        else: hi = mid

    a.insert(lo, x)
