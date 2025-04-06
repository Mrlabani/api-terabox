SIZE_UNITS = ['B', 'KB', 'MB', 'GB', 'TB']

def get_readable_file_size(size):
    i = 0
    while size >= 1024 and i < len(SIZE_UNITS) - 1:
        size /= 1024
        i += 1
    return f"{size:.2f} {SIZE_UNITS[i]}"
