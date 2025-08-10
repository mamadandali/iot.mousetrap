import sys
import numpy as np
from PIL import Image
import tflite_runtime.interpreter as tflite

# Load labels
with open('coco-labels-paper.txt', 'r') as f:
    labels = [line.strip() for line in f.readlines()]

# Load TFLite model
interpreter = tflite.Interpreter(model_path='coco_ssd_mobilenet_v2_320_float.tflite')
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

def preprocess(image):
    image = image.resize((320, 320))
    image_np = np.array(image)
    input_data = image_np / 255.0  # normalize
    input_data = np.expand_dims(input_data.astype(np.float32), axis=0)
    return input_data

def detect_apple_size(image_path):
    image = Image.open(image_path).convert('RGB')
    orig_width, orig_height = image.size

    input_data = preprocess(image)

    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()

    boxes = interpreter.get_tensor(output_details[0]['index'])[0]   # bounding boxes
    classes = interpreter.get_tensor(output_details[1]['index'])[0] # class indexes
    scores = interpreter.get_tensor(output_details[2]['index'])[0]  # confidence scores
    count = int(interpreter.get_tensor(output_details[3]['index'])[0])

    for i in range(count):
        if scores[i] >= 0.5:
            class_id = int(classes[i])
            label = labels[class_id]
            if label == 'apple':
                ymin, xmin, ymax, xmax = boxes[i]
                box_width = (xmax - xmin) * orig_width
                box_height = (ymax - ymin) * orig_height
                print(f"Apple detected!")
                print(f"Bounding box size in pixels: width = {box_width:.1f}, height = {box_height:.1f}")
                return

    print("Apple not detected with confidence >= 50%")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 detect_apple.py path_to_image.jpg")
        sys.exit(1)

    detect_apple_size(sys.argv[1])
