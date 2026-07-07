from typing import Literal


class ColorDyes():
    _TColorDyes = Literal[
        "white",
        "orange",
        "magenta",
        "light_blue",
        "yellow",
        "lime",
        "pink",
        "gray",
        "light_gray",
        "cyan",
        "purple",
        "blue",
        "brown",
        "green",
        "red",
        "black"
    ]
    _Udyes: list[_TColorDyes] = [ "white", "orange", "magenta", "light_blue", "yellow", "lime", "pink", "gray", "light_gray", "cyan", "purple", "blue", "brown", "green", "red", "black" ]
    _Udye_value: list[int] = [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15 ]
    _Udye_map: dict[_TColorDyes, int] = {
        dye: value for dye, value in zip(_Udyes, _Udye_value)
    }

    @staticmethod
    def get_dye_color(dye: _TColorDyes) -> int:
        return ColorDyes._Udye_map[dye]
    
    @staticmethod
    def get_dye_color_name(value: int) -> _TColorDyes | None:
        for dye, dye_value in ColorDyes._Udye_map.items():
            if dye_value == value:
                return dye
        return None