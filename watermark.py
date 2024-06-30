import os
from PIL import Image, ImageEnhance
from psd_tools import PSDImage

def convert_psd_to_png(psd_path, png_path):
    psd = PSDImage.open(psd_path)
    composite = psd.topil()
    composite.save(png_path)

def add_watermark(input_image_path, watermark_image_path, output_image_path, watermark_opacity=0.4):
    # Open the main image
    base_image = Image.open(input_image_path).convert("RGBA")
    
    # Open the watermark image
    watermark = Image.open(watermark_image_path).convert("RGBA")

    # Adjust the opacity of the watermark
    alpha = watermark.split()[3]  # Get the alpha channel
    alpha = ImageEnhance.Brightness(alpha).enhance(watermark_opacity)  # Apply opacity
    watermark.putalpha(alpha)  # Put the alpha channel back

    # Create a new image with the same size as the base image
    watermark_layer = Image.new('RGBA', base_image.size, (0, 0, 0, 0))

    # Tile the watermark image over the new image
    for y in range(0, base_image.size[1], watermark.size[1]):
        for x in range(0, base_image.size[0], watermark.size[0]):
            watermark_layer.paste(watermark, (x, y), watermark)

    # Combine the base image with the watermark layer
    combined = Image.alpha_composite(base_image, watermark_layer)

    # Convert the combined image to RGB and save it as a PNG
    combined = combined.convert("RGB")
    combined.save(output_image_path, "PNG", quality=95)

# Define input and output folders
input_folder = 'D:/watermark_CH/img_CH/goc'
output_folder = 'D:/watermark_CH/img_CH/jpg3'
watermark_psd_path = 'D:/watermark_CH/img_CH/watermark.psd'
watermark_png_path = 'D:/watermark_CH/img_CH/watermark.png'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Convert PSD to PNG
convert_psd_to_png(watermark_psd_path, watermark_png_path)

# Process each image in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith('.jpg'):
        input_image_path = os.path.join(input_folder, filename)
        output_image_path = os.path.join(output_folder, filename.replace('.jpg', '.png'))

        # Add watermark to the image
        add_watermark(input_image_path, watermark_png_path, output_image_path)

        print(f'Watermarked image saved as {output_image_path}')
