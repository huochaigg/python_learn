"""V1-04 循环：for、while、range、break / continue。

运行：uv run python lessons/v1_basics/04_loops.py
"""

print("for + range：从 0 数到 4")
for i in range(5):
    print("  i =", i)

print("for 遍历字符串")
for ch in "hi":
    print("  ch =", ch)

print("while：累加到大于 10 停止")
total = 0
n = 1
while total <= 10:
    total += n
    n += 1
print("  total =", total, "n =", n)

print("break：遇到 3 立刻结束循环")
for i in range(10):
    if i == 3:
        break
    print("  i =", i)

print("continue：跳过偶数，只打印奇数")
for i in range(6):
    if i % 2 == 0:
        continue
    print("  奇数 i =", i)

print("enumerate：同时拿到下标和元素")
for idx, fruit in enumerate[str](["apple", "banana"]):
    print(f"  {idx}: {fruit}")

if __name__ == "__main__":
    print("\n--- 04 循环 运行完毕 ---")
