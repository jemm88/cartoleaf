from .base import CustomIcon


def custom_pin_icon(
    background_color: str = "#693",
    text_color: str = "#fff",
    inner_text: str = "",
    inner_html: str | None = None,
    name_type: str = "default",
    inner_circle: bool = False,
    icon_wh: int = 33,
    inner_bg: str = "#fff",
    font_size: int = 15,
    font_weight: int = 400,
    inner_wh: int = 70,
) -> CustomIcon:
    """
    Creates a custom pin-shaped marker icon.

    This helper returns a CartoLeaf CustomIcon using inline HTML and CSS.
    It creates a rotated teardrop-style map pin and supports plain text,
    custom inner HTML, Bootstrap icons, and optional inner circle styling.

    Parameters
    ----------
    background_color : str, default="#693"
        Background color of the pin. Accepts any valid CSS color value.

    text_color : str, default="#fff"
        Text or icon color inside the pin.

    inner_text : str, default=""
        Plain text displayed inside the pin.

    inner_html : str | None, default=None
        Custom HTML displayed inside the pin. If provided, this takes
        precedence over inner_text.

    name_type : str, default="default"
        Name used to generate unique CSS class names for the icon.
        Useful when creating multiple pin styles on the same map.

    inner_circle : bool, default=False
        Whether to render the inner content inside a circular background.

    icon_wh : int, default=33
        Width and height of the icon in pixels.

    inner_bg : str, default="#fff"
        Background color of the inner circle when inner_circle=True.

    font_size : int, default=15
        Font size of the inner text in pixels.

    font_weight : int, default=400
        Font weight of the inner text.

    inner_wh : int, default=70
        Width and height of the inner circle as a percentage of the pin size.

    Returns
    -------
    CustomIcon
        A CustomIcon instance that can be passed into a CartoLeaf Marker.
    """
    css_class = f"cartoleaf-marker-{name_type}"
    pin_class = f"{css_class}-pin"

    content = inner_html if inner_html is not None else inner_text

    if inner_circle:
        span_css = f"""
        .{pin_class} span {{
            width: {inner_wh}%;
            height: {inner_wh}%;
            border-radius: 50%;
            background: {inner_bg};
            color: {text_color};
            display: flex;
            align-items: center;
            justify-content: center;
            transform: rotate(45deg);
            font-size: {font_size}px;
            font-weight: {font_weight};
        }}
        """
    else:
        span_css = f"""
        .{pin_class} span {{
            transform: rotate(45deg);
            font-size: {font_size}px;
            font-weight: {font_weight};
            color: {text_color};
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        """

    html = f"""
    <style>
        .{css_class} {{
            width: {icon_wh}px;
            height: {icon_wh}px;
            position: relative;
        }}

        .{pin_class} {{
            position: absolute;
            left: 50%;
            bottom: 0;
            width: {icon_wh}px;
            height: {icon_wh}px;
            background: {background_color};
            color: {text_color};
            border-radius: 50% 50% 50% 0;
            transform: translateX(-50%) rotate(-45deg);
            transform-origin: center center;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 0 2px #555;
            cursor: pointer;
            box-sizing: border-box;
        }}

        {span_css}

        .{pin_class} span svg {{
            width: 70%;
            height: 70%;
            display: block;
        }}

        .{pin_class} span svg path {{
            fill: {text_color};
        }}
    </style>

    <div class="{css_class}">
        <div class="{pin_class}">
            <span>{content}</span>
        </div>
    </div>
    """

    return CustomIcon(
        html=html,
        icon_size=(icon_wh, icon_wh),
        icon_anchor=(icon_wh // 2, icon_wh),
        popup_anchor=(0, -icon_wh),
        class_name="cartoleaf-div-icon",
    )

def bootstrap_icon(name: str) -> str:
    return f'<i class="bi bi-{name}"></i>'