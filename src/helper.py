from PIL import Image, ImageDraw

def draw_bounding_boxes(image_path: str, boxes: list) -> Image:
    image = Image.open(image_path).convert("RGB")
    draw = ImageDraw.Draw(image)
    
    image_width, image_height = image.size
    
    for box in boxes:
        absolute_box = [
        box[0] * image_width,
        box[1] * image_height,
        box[2] * image_width,
        box[3] * image_height
    ]
        draw.rectangle(absolute_box, outline="red", width=5)
    
    return image

