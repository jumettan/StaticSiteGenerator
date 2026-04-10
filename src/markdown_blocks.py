from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
    
def block_to_block_type(markdown):
    lines = markdown.split("\n")

    if markdown.startswith("```") and markdown.endswith("```"):
        return BlockType.CODE

    if lines[0].startswith("#"):
        count = len(lines[0]) - len(lines[0].lstrip("#"))
        if 1 <= count <= 6 and lines[0][count] == " ":
            return BlockType.HEADING

    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    is_ordered = True
    for i, line in enumerate(lines, start=1):
        if not line.startswith(f"{i}. "):
            is_ordered = False
            break
    if is_ordered:
        return BlockType.ORDERED_LIST

    # 🔹 DEFAULT
    return BlockType.PARAGRAPH