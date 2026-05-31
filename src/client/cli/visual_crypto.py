import random
import qrcode
from PIL import Image

def generate_visual_shares(data: str, prefix: str = "recovery"):
    """Generate QR Code visual shares for the given data."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4
    )
    qr.add_data(data)
    qr.make(fit=True)

    img_qr = qr.make_image(fill_color="black", back_color="white").convert("1")
    width, height = img_qr.size

    out_width, out_height = width * 2, height * 2
    share1 = Image.new("1", (out_width, out_height))
    share2 = Image.new("1", (out_width, out_height))

    pixels1 = share1.load()
    pixels2 = share2.load()
    qr_pixels = img_qr.load()

    patterns = [
        [(0, 255), (255, 0)], # Diagonal 1
        [(255, 0), (0, 255)], # Diagonal 2
        [(0, 0), (255, 255)], # Horizontal 1
        [(255, 255), (0, 0)], # Horizontal 2
        [(0, 255), (0, 255)], # Vertical 1
        [(255, 0), (255, 0)], # Vertical 2
    ]

    for y in range(height):
        for x in range(width):
            pixel = qr_pixels[x, y]
            
            pat = random.choice(patterns)
            
            pixels1[x*2, y*2] = pat[0][0]
            pixels1[x*2+1, y*2] = pat[0][1]
            pixels1[x*2, y*2+1] = pat[1][0]
            pixels1[x*2+1, y*2+1] = pat[1][1]
            
            if pixel == 255:
                pixels2[x*2, y*2] = pat[0][0]
                pixels2[x*2+1, y*2] = pat[0][1]
                pixels2[x*2, y*2+1] = pat[1][0]
                pixels2[x*2+1, y*2+1] = pat[1][1]
            else:
                pixels2[x*2, y*2] = 255 - pat[0][0]
                pixels2[x*2+1, y*2] = 255 - pat[0][1]
                pixels2[x*2, y*2+1] = 255 - pat[1][0]
                pixels2[x*2+1, y*2+1] = 255 - pat[1][1]

    file_share1 = f"{prefix}_share1.png"
    file_share2 = f"{prefix}_share2.png"
    share1.save(file_share1)
    share2.save(file_share2)

    combined = Image.new("1", (out_width, out_height))
    comb_pixels = combined.load()
    for y in range(out_height):
        for x in range(out_width):
            comb_pixels[x, y] = min(pixels1[x, y], pixels2[x, y])

    file_combined = f"{prefix}_combined.png"
    combined.save(file_combined)

    return file_share1, file_share2, file_combined