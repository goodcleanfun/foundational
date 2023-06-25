import importlib
import pkgutil


def import_submodules(package, recursive=True):
    """Import all submodules of a module, recursively, including subpackages

    :param package: package (name or actual module)
    :type package: str | module
    :rtype: dict[str, types.ModuleType]
    """
    q = [package]

    results = {}

    while q:
        package = q.pop()

        if isinstance(package, str):
            package = importlib.import_module(package)

        for _loader, name, is_pkg in pkgutil.walk_packages(package.__path__):
            full_name = package.__name__ + "." + name
            results[full_name] = importlib.import_module(full_name)
            if recursive and is_pkg:
                q.append(full_name)
    return results
