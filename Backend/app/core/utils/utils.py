# app/core/utils/utils.py
def safe_execute(func, error_message: str):
    try:
        return func()
    except Exception as e:
        raise SystemExit(f"{error_message}: {e}")
