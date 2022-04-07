def check_spn(lower, up):
    lower, up = lower.split(), up.split()
    low_x, low_y = lower
    up_x, up_y = up
    up_x, low_x, up_y, low_y = float(up_x), float(low_x), float(up_y), float(low_y)
    x = up_x - low_x
    y = up_y - low_y
    x = float(str(x)[:5])
    y = float(str(y)[:5])
    return x, y