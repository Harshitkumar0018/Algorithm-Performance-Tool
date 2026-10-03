"""Headless smoke test of the Streamlit app (no browser needed)."""
from streamlit.testing.v1 import AppTest

at = AppTest.from_file("app.py", default_timeout=120).run()
assert not at.exception, at.exception
for key in ["single_run", "search_run", "code_run", "auto_run"]:
    at.button(key=key).click().run()
    assert not at.exception, (key, at.exception)
    print(key, "ok")
