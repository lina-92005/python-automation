from PIL import Image, ImageDraw, ImageFont
import os

# 1️⃣ Input: folder containing images
while True:
    folder_path = input("Enter the folder path containing images: ").strip().strip('"')  # dont add "" just the address
    if os.path.exists(folder_path):
        break
    print("❌ Folder not found! Please try again.")

# 2️⃣ List all images (jpg, png) in folder order (no auto-sorting)
images_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
if not images_files:
    print("❌ No images found in the folder.")
    exit()

# 3️⃣ Ask if user wants to reorder
print("\n📂 Images found in folder order:")
for idx, name in enumerate(images_files, start=1):
    print(f"{idx}. {name}")

reorder_choice = input("\nDo you want to reorder them? (yes/no): ").strip().lower()
if reorder_choice == "yes":
    while True:
        try:
            new_order = input("Enter new order as space-separated numbers (e.g., 3 1 2 ...): ").strip()
            new_indices = list(map(int, new_order.split()))
            if sorted(new_indices) != list(range(1, len(images_files) + 1)):
                raise ValueError
            images_files = [images_files[i - 1] for i in new_indices]
            break
        except Exception:
            print("❌ Invalid order. Please try again.")

# 4️⃣ Output PDF name
output_pdf_name = input("Enter output PDF name (without .pdf): ").strip() + ".pdf"

# 5️⃣ Optional watermark
add_watermark = input("Do you want to add a watermark? (yes/no): ").strip().lower()
watermark_text = ""
if add_watermark == "yes":
    watermark_text = input("Enter watermark text: ")

# 6️⃣ Choose image scaling mode (stretch vs fit)
scaling_mode = input("Choose image scaling mode - (stretch/fit): ").strip().lower()
if scaling_mode not in ["stretch", "fit"]:
    scaling_mode = "stretch"  # default to stretch

# 7️⃣ Convert images to PDF
pdf_images = []

# Use first image size as reference (PDF page size)
first_img = Image.open(os.path.join(folder_path, images_files[0])).convert("RGB")
page_width, page_height = first_img.size

for img_file in images_files:
    img_path = os.path.join(folder_path, img_file)
    img = Image.open(img_path).convert("RGB")

    if scaling_mode == "stretch":
        # Stretch to full page size
        img = img.resize((page_width, page_height))
    else:  # fit
        # Fit inside while keeping aspect ratio
        img.thumbnail((page_width, page_height))
        new_img = Image.new("RGB", (page_width, page_height), (255, 255, 255))
        paste_x = (page_width - img.width) // 2
        paste_y = (page_height - img.height) // 2
        new_img.paste(img, (paste_x, paste_y))
        img = new_img

    draw = ImageDraw.Draw(img)

    # ✅ Add watermark (bottom-right)
    if watermark_text:
        font_size = max(20, img.width // 20)  # dynamic font size
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        text_width, text_height = draw.textbbox((0, 0), watermark_text, font=font)[2:4]
        position = (img.width - text_width - 10, img.height - text_height - 10)
        draw.text(position, watermark_text, fill=(0, 0, 0), font=font)  # black watermark

    # ✅ Add page number (bottom-center)
    page_num = f"{len(pdf_images) + 1}"
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except:
        font = ImageFont.load_default()
    text_width, text_height = draw.textbbox((0, 0), page_num, font=font)[2:4]
    position = ((img.width - text_width) // 2, img.height - text_height - 10)
    draw.text(position, page_num, fill=(0, 0, 0), font=font)

    pdf_images.append(img)

# Save all images into one PDF
output_path = os.path.join(folder_path, output_pdf_name)
pdf_images[0].save(output_path, save_all=True, append_images=pdf_images[1:])
print(f"✅ PDF created successfully: {output_path}")
