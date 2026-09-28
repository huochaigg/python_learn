from agents import set_tracing_disabled


def pytest_configure() -> None:
    # 单测不向 OpenAI Tracing Dashboard 上报。
    set_tracing_disabled(True)
