"""V9-02 Iterator：记录「遍历到哪里」的游标。

学习目标：
1. 分清 Iterable（数据来源）和 Iterator（读取游标）。
2. 看到同一个 iterator 连续读时不会自动从头开始。
3. 确认原 list 还在，被消耗的是 iterator，不是源数据。

运行：uv run python lessons/v9/02_iterator.py
"""

nums = [1, 2, 3]
print("源数据 nums =", nums)

# Iterator：真正记录「当前读到哪」的对象。
# 比喻：有点像数据库 cursor 的「当前位置」。只是帮助理解，协议并不等价。
# JS/TS 对比：iterator.next() 也是有状态的，不会每次从 0 重来。
iterator = iter(nums)
print("iterator 类型 =", type(iterator))

print("第一次消费 iterator:")
print(" ", next(iterator), next(iterator))

print("接着消费同一个 iterator（不会回到 1）:")
print(" ", next(iterator))

print("源 list 还在 =", nums)

# 再从同一份 list 拿一个「新游标」，才会从头开始。
fresh = iter(nums)
print("新的 iterator 从头开始 =", next(fresh))

if __name__ == "__main__":
    print("\n--- 02 Iterator 运行完毕 ---")

# 本文件重点：
# 1. Iterable 是数据来源；Iterator 是读取游标，会保存消费位置。
# 2. 同一个 iterator 一路往前，不会自动重置。
# 3. 耗掉 iterator 不会把原 list 删掉。
# 4. 想再从头遍历：重新 iter(源数据)，或再 for 一遍源数据。
