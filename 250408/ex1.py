import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import lognorm

# 使用者輸入參數
mu = float(input("請輸入 μ (mu) 的值："))
sigma = float(input("請輸入 σ (sigma) 的值："))

# 計算對數常態分布的參數
s = sigma
scale = np.exp(mu)

# 定義 x 範圍
x = np.linspace(0.01, 10, 500)

# 計算累積分布函數 (CDF)
cdf = lognorm.cdf(x, s, scale=scale)

# 繪製圖形
plt.figure(figsize=(8, 6))
plt.plot(x, cdf, label='Lognormal CDF', color='blue')
plt.title('Lognormal Cumulative Distribution Function (CDF)')
plt.xlabel('x')
plt.ylabel('CDF')
plt.grid(True)
plt.legend()

# 儲存為 JPG 檔案
plt.savefig('lognormal_cdf.jpg', format='jpg')
plt.show()