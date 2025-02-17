import cv2
import os
from pyzbar.pyzbar import decode

# Input and output directories
input_dir = "qr_images"  # Folder containing QR code images
output_dir = "cropped_qr"  # Folder to save cropped QR codes

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Loop through all images in the directory
for filename in os.listdir(input_dir):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):  # Process only image files
        img_path = os.path.join(input_dir, filename)

        # Read the image
        img = cv2.imread(img_path)
        if img is None:
            print(f"Error: Could not read {filename}. Skipping...")
            continue

        # Convert to grayscale (ZBar works better with grayscale images)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Detect QR codes using ZBar
        decoded_objs = decode(gray)

        if decoded_objs:
            print(f"✅ QR Code detected in: {filename}")

            for obj in decoded_objs:
                x, y, w, h = obj.rect  # Get bounding box coordinates
                print(f"🔍 Cropping region for {filename}: x={x}, y={y}, w={w}, h={h}")

                # Crop QR code
                cropped_qr = img[y:y+h, x:x+w]

                # Ensure cropped image is valid
                if cropped_qr.size == 0:
                    print(f"⚠️ Skipping {filename}: Cropped image is empty.")
                    continue

                # Save cropped QR code with the same filename
                output_path = os.path.join(output_dir, filename)
                cv2.imwrite(output_path, cropped_qr)

        else:
            print(f"❌ QR Code not detected in: {filename}")

print("🎉 Processing completed!")
