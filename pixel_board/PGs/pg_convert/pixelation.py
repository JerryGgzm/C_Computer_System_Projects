from PIL import Image, ImageColor


def pixelation(filename, width, height, palette):
    image = Image.open(filename).convert('RGB')
    availible_palette = {color: list(ImageColor.getcolor(color, "RGB")) for color in palette}
    print("\navailible palette:", availible_palette)
    new_image = Image.new(mode = 'P', size = (height, width))
    rgb_as_list = []
    for rgb_value in list(availible_palette.values()):
        rgb_as_list += rgb_value
    new_image.putpalette(rgb_as_list)
    
    new_img = (image.quantize(palette=new_image, dither=0)).convert('RGB')
    # new_img = Image.fromarray(conv, mode="RGB")
    # print([[palette.index(f"#{'%02X%02X%02X'%new_img.getpixel((i, j))}") for j in range(width)] for i in range(height)],"pixelation.py output:")
    return [[palette.index(f"#{'%02X%02X%02X'%new_img.getpixel((i, j))}") for i in range(height)] for j in range(width)]