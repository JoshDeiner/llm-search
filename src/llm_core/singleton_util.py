# llm_core/singleton_util.py


def get_instance(cls, *args, **kwargs):
    """
    Generic Singleton access method.
    Ensures only one instance of the given class is created.

    Args:
        cls: The class for which to return a singleton instance.
        *args, **kwargs: Arguments to initialize the class if needed.

    Returns:
        The singleton instance of the class.
    """
    if not hasattr(cls, "_instance") or cls._instance is None:
        cls._instance = cls(*args, **kwargs)
    return cls._instance
