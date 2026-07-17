def get_total_pages(total_items: int, page_size: int) -> int:
    return max(1, (total_items + page_size - 1) // page_size)

def get_offset(page: int, page_size: int) -> int:
    return (page - 1) * page_size