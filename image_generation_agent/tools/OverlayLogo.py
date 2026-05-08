"""Overlay an official logo file onto a generated background image using Pillow.

This tool is DETERMINISTIC — it never passes the logo to an AI model.
The logo is composited pixel-accurately using Pillow RGBA alpha compositing.
Use this instead of CombineImages for any client logo placement.
"""

import os
from pathlib import Path
from typing import Literal, Optional

from PIL import Image
from pydantic import Field, field_validator

from agency_swarm import BaseTool, ToolOutputImage, ToolOutputText
from .utils.image_io import image_to_base64_jpeg


class OverlayLogo(BaseTool):
    """
    Overlay an official logo PNG onto a generated background image using Pillow.

    The logo is NEVER passed to an AI model — this is pure Pillow compositing.
    Alpha transparency in the logo PNG is fully preserved.

    Saves two files:
    - raw background (unchanged copy of background_image_path, for reference)
    - final graphic with logo composited on top
    """

    background_image_path: str = Field(
        ...,
        description="Absolute path to the generated background PNG.",
    )
    logo_path: str = Field(
        ...,
        description="Absolute path to the official logo PNG file (must be real file, not AI-generated).",
    )
    output_path: str = Field(
        ...,
        description=(
            "Absolute path for the final composited output PNG. "
            "Example: C:/path/to/clients/oxford-golf-academy/outputs/june_2026/graphics/oga_post1_final.png"
        ),
    )
    position: Literal["top-left", "top-right", "bottom-left", "bottom-right", "top-center", "bottom-center"] = Field(
        default="top-left",
        description="Where to place the logo on the background.",
    )
    logo_scale: float = Field(
        default=0.22,
        description=(
            "Logo width as a fraction of the background width (0.0–0.5). "
            "0.22 = logo takes up 22% of background width. Adjust for visual balance."
        ),
    )
    padding_px: int = Field(
        default=32,
        description="Padding in pixels between the logo and the nearest edges.",
    )
    logo_opacity: float = Field(
        default=1.0,
        description="Logo opacity (0.0 = transparent, 1.0 = fully opaque). Default 1.0.",
    )

    @field_validator("background_image_path", "logo_path", "output_path")
    @classmethod
    def _not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("path must not be empty")
        return v

    @field_validator("logo_scale")
    @classmethod
    def _validate_scale(cls, v: float) -> float:
        if not (0.05 <= v <= 0.5):
            raise ValueError("logo_scale must be between 0.05 and 0.5")
        return v

    @field_validator("logo_opacity")
    @classmethod
    def _validate_opacity(cls, v: float) -> float:
        if not (0.0 <= v <= 1.0):
            raise ValueError("logo_opacity must be between 0.0 and 1.0")
        return v

    def run(self) -> list:
        # Validate inputs
        if not os.path.isfile(self.background_image_path):
            return [ToolOutputText(type="text", text=f"Error: Background image not found: {self.background_image_path}")]
        if not os.path.isfile(self.logo_path):
            return [ToolOutputText(type="text", text=(
                f"Error: Logo file not found: {self.logo_path}\n"
                f"Logo must be added manually. Mark graphic as: 'Logo overlay pending — add official logo file to assets/'"
            ))]

        # Load background — work in RGBA
        bg = Image.open(self.background_image_path).convert("RGBA")
        bg_w, bg_h = bg.size

        # Load logo — preserve transparency
        logo = Image.open(self.logo_path).convert("RGBA")

        # Scale logo to target width
        target_logo_w = int(bg_w * self.logo_scale)
        logo_aspect = logo.height / logo.width
        target_logo_h = int(target_logo_w * logo_aspect)
        logo = logo.resize((target_logo_w, target_logo_h), Image.Resampling.LANCZOS)

        # Apply opacity if less than 1.0
        if self.logo_opacity < 1.0:
            r, g, b, a = logo.split()
            a = a.point(lambda x: int(x * self.logo_opacity))
            logo = Image.merge("RGBA", (r, g, b, a))

        # Calculate position
        pad = self.padding_px
        lw, lh = logo.size

        if self.position == "top-left":
            x, y = pad, pad
        elif self.position == "top-right":
            x, y = bg_w - lw - pad, pad
        elif self.position == "bottom-left":
            x, y = pad, bg_h - lh - pad
        elif self.position == "bottom-right":
            x, y = bg_w - lw - pad, bg_h - lh - pad
        elif self.position == "top-center":
            x, y = (bg_w - lw) // 2, pad
        elif self.position == "bottom-center":
            x, y = (bg_w - lw) // 2, bg_h - lh - pad
        else:
            x, y = pad, pad

        # Composite
        canvas = bg.copy()
        canvas.paste(logo, (x, y), mask=logo)

        # Save final output
        output_path = Path(self.output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        final_rgb = canvas.convert("RGB")
        final_rgb.save(str(output_path), format="PNG")

        # Save raw background copy alongside final (in same folder, _raw suffix)
        raw_path = output_path.with_stem(output_path.stem + "_raw_bg")
        bg.convert("RGB").save(str(raw_path), format="PNG")

        preview_b64 = image_to_base64_jpeg(final_rgb)

        outputs = [
            ToolOutputText(type="text", text=(
                f"Logo overlay complete.\n"
                f"Final graphic (with logo): {output_path}\n"
                f"Raw background (no logo):  {raw_path}\n"
                f"Logo source: {self.logo_path}\n"
                f"Position: {self.position}, Scale: {self.logo_scale:.0%} of width, Padding: {self.padding_px}px"
            )),
            ToolOutputImage(type="image", image_url=f"data:image/jpeg;base64,{preview_b64}", detail="auto"),
        ]
        return outputs
