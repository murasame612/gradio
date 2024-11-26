import os

def generate_html_with_images(image_paths):
    html_content = '<div class="image-container">'
    for path in image_paths:
        # 使用绝对路径
        abs_path = os.path.abspath(path)
        html_content += f'<img src="file://{abs_path}" style="margin: 10px; max-width: 200px; max-height: 200px;">'
    html_content += '</div>'
    return html_content

def get_image_paths(user):
    # 获取用户目录下的所有图片路径
    user_dir = os.path.join("./user", user, 'image')
    if not os.path.exists(user_dir):
        return []
    return [os.path.join(user_dir, img) for img in os.listdir(user_dir) if img.endswith(('.png', '.jpg', '.jpeg'))]

def update_images():
    return "<img src=http://127.0.0.1:5000/image/1.png>"
