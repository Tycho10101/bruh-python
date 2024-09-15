from flask import Flask, request, render_template, send_file, redirect, url_for, flash
from PIL import Image
import os, io, base64, tempfile

app = Flask(__name__)
app.secret_key = 'themostbruhkey'

MAX_PIXELS = 40000

# Temporary directory for storing files
temp_dir = tempfile.gettempdir()

def check_image_size(width, height):
    return width * height <= MAX_PIXELS

def resize_image(img, max_pixels):
    width, height = img.size
    total_pixels = width * height
    if total_pixels <= max_pixels:
        return img, False  # No resizing needed, image is already within limits
    
    scaling_factor = (max_pixels / total_pixels) ** 0.5
    new_width = int(width * scaling_factor)
    new_height = int(height * scaling_factor)
    resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    return resized_img, True

@app.route('/')
def home():
    return render_template('home.html')

# Convert Image to .bruh
@app.route('/convert_to_bruh')
def convert_to_bruh_page():
    return render_template('convert_to_bruh.html')

@app.route('/process_bruh', methods=['POST'])
def process_bruh():
    if 'image' not in request.files or request.files['image'].filename == '':
        return "No image uploaded"
    
    file = request.files['image']
    img = Image.open(file)
    img = img.convert('RGB')

    # Resize if necessary
    img, resized = resize_image(img, MAX_PIXELS)

    if resized:
        flash("Image was too large and has been resized to fit within the limit.")

    width, height = img.size
    bwidth = width.to_bytes(length=4, byteorder='big')
    bheight = height.to_bytes(length=4, byteorder='big')

    bruh_data = bwidth + bheight
    for iy in range(height):
        for ix in range(width):
            r, g, b = img.getpixel((ix, iy))
            hex_value = "{:02x}{:02x}{:02x}".format(r, g, b)
            bruh_data += hex_value.encode('utf-8')
        bruh_data += b'\n'

    # Save the .bruh file to a temporary file
    temp_file_path = os.path.join(temp_dir, 'converted.bruh')
    with open(temp_file_path, 'wb') as temp_file:
        temp_file.write(bruh_data)

    return redirect(url_for('download_bruh'))

@app.route('/download_bruh')
def download_bruh():
    temp_file_path = os.path.join(temp_dir, 'converted.bruh')

    if os.path.exists(temp_file_path):
        return render_template('download_bruh.html', file_ready=True)
    else:
        return render_template('download_bruh.html', file_ready=False)

@app.route('/download_file')
def download_file():
    temp_file_path = os.path.join(temp_dir, 'converted.bruh')

    if os.path.exists(temp_file_path):
        return send_file(temp_file_path, as_attachment=True, download_name="converted.bruh", mimetype='application/octet-stream')
    else:
        return "File not found", 404

# Route for converting .bruh to image
@app.route('/convert_to_image')
def convert_to_image_page():
    return render_template('convert_to_image.html')

@app.route('/process_image', methods=['POST'])
def process_image():
    if 'bruhfile' not in request.files or request.files['bruhfile'].filename == '':
        return "No .bruh file uploaded"
    
    file = request.files['bruhfile']
    bruh_data = file.read()

    # Extract width and height from the first 8 bytes
    width = int.from_bytes(bruh_data[0:4], byteorder='big')
    height = int.from_bytes(bruh_data[4:8], byteorder='big')

    pixel_data = bruh_data[8:].split(b'\n')

    # Create a new image
    img = Image.new("RGB", (width, height))
    for iy, line in enumerate(pixel_data):
        if line:
            hex_colors = [line[i:i+6].decode('utf-8') for i in range(0, len(line), 6)]
            for ix, hex_color in enumerate(hex_colors):
                r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
                img.putpixel((ix, iy), (r, g, b))

    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)

    return send_file(img_io, as_attachment=True, download_name="converted.png", mimetype='image/png')

# Route for viewing .bruh as an image
@app.route('/view_bruh')
def view_bruh_page():
    return render_template('view_bruh.html')

@app.route('/display_bruh', methods=['POST'])
def display_bruh():
    if 'bruhfile' not in request.files or request.files['bruhfile'].filename == '':
        return "No .bruh file uploaded"
    
    file = request.files['bruhfile']
    bruh_data = file.read()

    # Extract width and height from the first 8 bytes
    width = int.from_bytes(bruh_data[0:4], byteorder='big')
    height = int.from_bytes(bruh_data[4:8], byteorder='big')

    pixel_data = bruh_data[8:].split(b'\n')

    # Create a new image
    img = Image.new("RGB", (width, height))
    for iy, line in enumerate(pixel_data):
        if line:
            hex_colors = [line[i:i+6].decode('utf-8') for i in range(0, len(line), 6)]
            for ix, hex_color in enumerate(hex_colors):
                r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
                img.putpixel((ix, iy), (r, g, b))

    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')

    return render_template('display_image.html', img_data=img_base64)

if __name__ == '__main__':
    app.run(debug=False)
