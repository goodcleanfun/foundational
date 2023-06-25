import resource
import sys


def get_current_process_memory_usage():
    """Gets current process memory usage (residence set size) in megabytes."""
    resource_data = resource.getrusage(resource.RUSAGE_SELF)
    if sys.platform == "darwin":
        return resource_data.ru_maxrss / (1024 * 1024)
    else:
        return resource_data.ru_maxrss / 1024
