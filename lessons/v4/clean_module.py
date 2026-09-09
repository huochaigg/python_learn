"""把逻辑放进函数，import 时不再自动干活。"""


def ping() -> str:
    """只有被调用时才执行。"""
    return "pong"


def main() -> None:
    print("clean_module.main() ->", ping())


if __name__ == "__main__":
    main()
