"""V22 速查：ForeignKey / relationship / 加载策略。

运行：uv run python lessons/v22/notes.py
"""

NOTES = """
ForeignKey vs relationship
  ForeignKey 是数据库列引用（OrderItem.order_id -> orders.id）。
  relationship 是 ORM 导航属性。orders 表没有 items 列。
  SQLAlchemy 常用 ForeignKey 推导 JOIN ON，但两者职责不同。

one-to-many / many-to-one
  Order.items: list[OrderItem]（一对多 collection）。
  OrderItem.order: 单个 Order（多对一 scalar）。
  ForeignKey 放在「多」的一方：OrderItem.order_id。

back_populates
  显式连接关系两端，表示同一个双向关系。
  SQLAlchemy 2.x 推荐它，不要把 legacy backref 当主写法。
  item.order = order 或 order.items.append(item)，另一端会同步。

lazy loading
  访问未加载 relationship 时自动补查询。
  session.get(Order, id) 之后读 order.items，常会再发一条 SELECT。

N+1
  查 N 个父对象，再循环访问 lazy collection，变成 1+N 条 SQL。
  这是 ORM 常见问题，不是 SQLAlchemy 独有。

selectinload
  eager loading。通常：父表一条 + 子表 WHERE parent_id IN (...) 一条。
  一对多集合很常用，不造成父行 JOIN 膨胀。

joinedload
  eager loading，用 JOIN 一次取回关系数据。
  collection 较大时父行在 Result 里会重复（行乘法）。
  需要 Result.unique() 对 ORM Entity 去重。这不是 SQL DISTINCT。
  不要认为「一条 SQL 一定比两条快」。

join vs joinedload
  join()：改查询本身，用于过滤/排序。
  joinedload()：加载 relationship。
  SQL 里都可能出现 JOIN，意图不同。

distinct / unique
  distinct() 生成 SQL DISTINCT。
  unique() 是 Result/ORM Entity 去重。

cascade
  默认 save-update, merge：add(父) 可带上未入库的子对象。
  all, delete-orphan 有删行风险，本课不作为业务默认配置。
"""


def main() -> None:
    print(NOTES)


if __name__ == "__main__":
    main()
    print("--- v22 notes 运行完毕 ---")
