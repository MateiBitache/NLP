"""Small SVG writer for report and presentation charts."""

from __future__ import annotations

from pathlib import Path

from .constants import EMOTIONS


COLORS = {
    "anger": "#d73027",
    "anticipation": "#fdae61",
    "disgust": "#7f3b08",
    "fear": "#6a51a3",
    "joy": "#1a9850",
    "sadness": "#4575b4",
    "surprise": "#00a6d6",
    "trust": "#66bd63",
}


def write_distribution_svg(
    path: str | Path,
    distribution: dict[str, int],
    *,
    title: str = "Predicted emotion distribution",
) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    width = 920
    height = 420
    margin_left = 150
    margin_right = 40
    margin_top = 58
    row_height = 38
    max_value = max(distribution.values(), default=1) or 1
    chart_width = width - margin_left - margin_right

    svg_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        f'<text x="{margin_left}" y="30" font-family="Arial, sans-serif" font-size="20" font-weight="700">{escape_xml(title)}</text>',
    ]

    for index, emotion in enumerate(EMOTIONS):
        count = distribution.get(emotion, 0)
        bar_y = margin_top + index * row_height
        bar_width = int(chart_width * count / max_value)
        color = COLORS[emotion]
        svg_lines.extend(
            [
                f'<text x="22" y="{bar_y + 21}" font-family="Arial, sans-serif" font-size="14" fill="#222">{emotion}</text>',
                f'<rect x="{margin_left}" y="{bar_y}" width="{chart_width}" height="24" rx="3" fill="#eeeeee"/>',
                f'<rect x="{margin_left}" y="{bar_y}" width="{bar_width}" height="24" rx="3" fill="{color}"/>',
                f'<text x="{margin_left + bar_width + 8}" y="{bar_y + 17}" font-family="Arial, sans-serif" font-size="13" fill="#222">{count}</text>',
            ]
        )

    svg_lines.append("</svg>")
    output_path.write_text("\n".join(svg_lines), encoding="utf-8")


def escape_xml(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )
