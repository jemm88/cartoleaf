from .icon import CustomIcon


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