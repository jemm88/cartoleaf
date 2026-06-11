from dataclasses import dataclass


@dataclass
class CustomIcon:
    html: str
    icon_size: tuple[int, int] = (33, 33)
    icon_anchor: tuple[int, int] = (16, 33)
    popup_anchor: tuple[int, int] = (0, -27)
    class_name: str = ""