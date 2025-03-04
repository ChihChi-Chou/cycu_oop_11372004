def absolute_value_wrong(x):
    if x < 0:
        return -x
    if x > 0:
        return x
    else:
        return 0
    6

# 讓使用者輸入數字
x = int(input("x : "))


# 計算並輸出絕對值
print("abs_x:", absolute_value_wrong(x))



def is_divisible(x, y):
    if x % y == 0:
        return True
    else:
        return False
    
x = int(input("x : "))
y = int(input("y : "))

if is_divisible(x, y):
    print(f"True")
else:
    print(f"False")
