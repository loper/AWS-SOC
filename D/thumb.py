def resize_thumbnail(thumbnail):
    # image and description
    prop_w = eval(thumbnail["srcw"])
    prop_h = eval(thumbnail["srch"])
    # thumbnail height
    dsth = 100
    if prop_w > prop_h:
        dstw = round(dsth / (prop_w/prop_h))
    else:
        dstw = round(dsth * (prop_h/prop_w))
    return (dsth, dstw)


thumbnail = {}
thumbnail["srcw"] = "56/100"
thumbnail["srch"] = "84/100"

print(resize_thumbnail(thumbnail))