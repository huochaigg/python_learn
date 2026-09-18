"""V21 速查：动态查询 / 分页 / count / exists。

运行：uv run python lessons/v21/notes.py
"""

NOTES = """
where
  Select.where(expr) 把 SQL Expression 放进 WHERE。
  User.age >= 18 不是立刻得到 Python bool，而是生成 SQL 比较。

and_ / 连续 where
  连续 .where(a).where(b)、.where(a, b)、.where(*conditions) 通常都是 AND。
  and_() 显式组合 AND；条件很多或要嵌套时有用，简单场景不必强行用。

or_
  生成 SQL OR。不要用 Python or 连接两个 SQL Expression。

in_
  生成 SQL IN (...)。不要和 Python `x in list` 混淆。

contains / like / ilike
  contains(k) 大致 LIKE '%k%'。
  like 是 SQL LIKE；ilike 是大小写不敏感 LIKE。
  各库大小写行为可能不同，本课不展开 collation。

动态 conditions
  conditions = []，有值再 append，最后 where(*conditions)。
  bool 用 `is not None`：`if active:` 会把 False 当成没筛选。

order_by / asc / desc
  生成 ORDER BY。分页必须明确稳定排序（例如 created_at DESC, id DESC）。
  sort_by 用白名单映射到列，禁止把前端字符串拼进 SQL。

limit / offset / slice
  offset 跳过多少行；limit 最多取多少行。
  页码：(page - 1) * page_size。
  slice(start, stop) 也能变成 LIMIT/OFFSET；主业务优先显式 offset/limit。

func.count
  func 构造 SQL 函数。COUNT 由数据库完成，不要查出全部 ORM 再 len()。
  count query 复用同一套 conditions，不要带 offset/limit。

session.scalar
  只要第一行第一列单个值，适合 COUNT / EXISTS。
  和 execute().scalars().all() 拿对象列表不是同一场景。

exists
  只问「有没有」，不加载完整对象。
  get：主键拿对象；scalar_one_or_none：按业务条件拿单对象；exists：只判断存在。
"""


def main() -> None:
    print(NOTES)


if __name__ == "__main__":
    main()
    print("--- v21 notes 运行完毕 ---")
