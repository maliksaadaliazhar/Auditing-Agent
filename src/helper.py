from PIL import Image, ImageDraw

def draw_bounding_boxes(image_path: str, boxes: list) -> Image:
    image = Image.open(image_path).convert("RGB")
    draw = ImageDraw.Draw(image)
    
    for box in boxes:
        draw.rectangle(box, outline="red", width=5)
    
    return

