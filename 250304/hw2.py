def gcd(a, b):
    # 使用輾轉相除法計算最大公因數
    if b == 0:
        return a
    return gcd(b , a % b)

# 輸入兩個整數
x , y = 7 , 49
print(f"gcd of {x} and {y} is: {gcd(x , y)}")

x , y = 11 , 121
print(f"gcd of {x} and {y} is: {gcd(x , y)}")