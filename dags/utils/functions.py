def can_i_run(**context) -> bool:
    return context["params"].get("can_i_run", False)
