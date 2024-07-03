import pkgutil
from pathlib import Path


def load_all_models() -> None:
    """Load all models from this folder."""
    __import__("db.models")  # noqa: WPS421
    # package_dir = Path(__file__).resolve().parent
    # modules = pkgutil.walk_packages(
    #     path=[str(package_dir)],
    #     prefix="db.",
    # )
    # for module in modules:
    #     print("module", module)
    #     __import__(module.name)  # noqa: WPS421
