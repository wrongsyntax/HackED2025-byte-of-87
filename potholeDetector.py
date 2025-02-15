from PIL import Image
from ultralytics import YOLO

model = YOLO('best_pothole_data.pt')
image_path = '121images.jpg'
img = Image.open(image_path)

results = model(img, conf=0.05)
results[0].save()