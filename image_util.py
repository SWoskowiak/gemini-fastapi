"""Utility functions for working with images."""
# pylint: disable=line-too-long
from typing import IO
import io
from PIL import Image

def make_thumbnail(file: IO, max_size: tuple[int, int]) -> bytes:
    """
    Create a thumbnail of an image and return it as bytes.

    The thumbnail will be resized to fit within the max_size dimensions while maintaining the original aspect ratio.

    Parameters :
        file (IO): The image file to create a thumbnail of.
        max_size (tuple[int, int]): A tuple specifying the maximum width and height of the thumbnail.

    Returns:
        bytes: The thumbnail image as bytes.
    """
    try:
        original_image = Image.open(file)
    except IOError as exc:
        raise ValueError("Invalid image file") from exc

    original_image.thumbnail(max_size)

    # Save the thumbnail to a byte stream
    thumbnail_bytes_io = io.BytesIO()
    original_image.save(thumbnail_bytes_io, format='JPEG')

    # Get the byte data from the byte stream
    thumbnail_bytes = thumbnail_bytes_io.getvalue()

    return thumbnail_bytes
