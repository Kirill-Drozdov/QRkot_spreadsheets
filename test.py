JS_CONST = {'a': 1, 'd': {'x': 1}}
# js_copy = JS_CONST.copy()
js_copy = JS_CONST
js_copy['d']['x'] = 2
print(JS_CONST['d']['x'])  # ??
print(js_copy['d']['x'])  # ??