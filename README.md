import math
import time

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from PIL import Image

NUM_RESULTS = 1917
NUM_CLASSES = 91

X_SCALE = 10.0
Y_SCALE = 10.0
H_SCALE = 5.0
W_SCALE = 5.0


def load_box_priors(filename):
    box_priors = []
    with open(filename) as f:
        count = 0
        for line in f:
            row = line.strip().split(' ')
            box_priors.append(row)
            count += 1
            if count == 4:
                break
    # Convert to float arrays for calculations
    box_priors = [list(map(float, arr)) for arr in box_priors]
    return box_priors


def load_labels(filename):
    my_labels = []
    with open(filename, 'r') as f:
        for line in f:
            my_labels.append(line.strip())
    return my_labels


def decode_center_size_boxes(locations, box_priors):
    """Calculate real bounding boxes from locations."""
    for i in range(NUM_RESULTS):
        ycenter = locations[i][0] / Y_SCALE * box_priors[2][i] + box_priors[0][i]
        xcenter = locations[i][1] / X_SCALE * box_priors[3][i] + box_priors[1][i]
        h = math.exp(locations[i][2] / H_SCALE) * box_priors[2][i]
        w = math.exp(locations[i][3] / W_SCALE) * box_priors[3][i]

        ymin = ycenter - h / 2.0
        xmin = xcenter - w / 2.0
        ymax = ycenter + h / 2.0
        xmax = xcenter + w / 2.0

        locations[i][0] = ymin
        locations[i][1] = xmin
        locations[i][2] = ymax
        locations[i][3] = xmax

    return locations


def iou(box_a, box_b):
    x_a = max(box_a[0], box_b[0])
    y_a = max(box_a[1], box_b[1])
    x_b = min(box_a[2], box_b[2])
    y_b = min(box_a[3], box_b[3])

    if x_b < x_a or y_b < y_a:
        return 0.0  # no overlap

    intersection_area = (x_b - x_a) * (y_b - y_a)

    box_a_area = (box_a[2] - box_a[0]) * (box_a[3] - box_a[1])
    box_b_area = (box_b[2] - box_b[0]) * (box_b[3] - box_b[1])

    return intersection_area / float(box_a_area + box_b_area - intersection_area)


def nms(predictions, iou_threshold, max_boxes):
    sorted_preds = sorted(predictions, key=lambda x: x[0], reverse=True)
    selected = []
    for pred in sorted_preds:
        if len(selected) >= max_boxes:
            break
        keep = True
        for s in selected:
            if iou(pred[3], s[3]) > iou_threshold:
                keep = False
                break
        if keep:
            selected.append(pred)
    return selected


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: python detect_apple.py path_to_image.jpg")
        sys.exit(1)

    image_file = sys.argv[1]
    model_file = "tflite_models/ssdlite_mobilenet_v2_coco.tflite"
    label_file = "tmp/coco_labels_list.txt"
    box_prior_file = "tmp/box_priors.txt"

    input_mean = 127.5
    input_std = 127.5
    min_score_percent = 60.0
    max_boxes = 10
    floating_model = False
    show_image = True
    alt_output_order = False

    # Load interpreter
    interpreter = tf.lite.Interpreter(model_path=model_file)
    interpreter.allocate_tensors()

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # Check input type
    if input_details[0]['dtype'] == np.float32:
        floating_model = True

    height = input_details[0]['shape'][1]
    width = input_details[0]['shape'][2]

    # Load image and preprocess
    img = Image.open(image_file).convert('RGB')
    orig_width, orig_height = img.size
    img_resized = img.resize((width, height))

    input_data = np.expand_dims(img_resized, axis=0)
    if floating_model:
        input_data = (np.float32(input_data) - input_mean) / input_std

    interpreter.set_tensor(input_details[0]['index'], input_data)

    start_time = time.time()
    interpreter.invoke()
    end_time = time.time()
    print(f"Inference time: {(end_time - start_time)*1000:.2f} ms")

    # Load box priors and labels
    box_priors = load_box_priors(box_prior_file)
    labels = load_labels(label_file)

    # Output indexes
    p_index = 0
    o_index = 1
    if alt_output_order:
        p_index, o_index = o_index, p_index

    predictions = np.squeeze(interpreter.get_tensor(output_details[p_index]['index']))
    output_classes = np.squeeze(interpreter.get_tensor(output_details[o_index]['index']))

    if not floating_model:
        p_scale, p_mean = output_details[p_index]['quantization']
        o_scale, o_mean = output_details[o_index]['quantization']

        predictions = (predictions - p_mean) * p_scale
        output_classes = (output_classes - o_mean) * o_scale

    decode_center_size_boxes(predictions, box_priors)

    # Collect detections per class
    pruned_predictions = [[] for _ in range(NUM_CLASSES)]

    for c in range(1, NUM_CLASSES):
        for r in range(NUM_RESULTS):
            score = 1. / (1. + math.exp(-output_classes[r][c]))
            if score > 0.01:
                rect = (
                    predictions[r][1] * width,
                    predictions[r][0] * orig_height,
                    predictions[r][3] * width,
                    predictions[r][2] * orig_height,
                )
                pruned_predictions[c].append((score, r, labels[c], rect))

    # Non-Max Suppression and gather final predictions
    final_predictions = []
    for c in range(1, NUM_CLASSES):
        filtered = nms(pruned_predictions[c], 0.5, max_boxes)
        final_predictions.extend(filtered)

    # Sort final predictions by score descending and limit to max_boxes
    final_predictions = sorted(final_predictions, key=lambda x: x[0], reverse=True)[:max_boxes]

    # Focus on apples only
    apple_label = 'apple'
    apple_detections = [p for p in final_predictions if p[2] == apple_label]

    if not apple_detections:
        print(f"No apple detected with confidence >= {min_score_percent}%")
    else:
        for score, _, label, rect in apple_detections:
            score_percent = score * 100
            if score_percent < min_score_percent:
                continue
            left, top, right, bottom = rect
            width_box = right - left
            height_box = bottom - top
            print(f"Apple detected with confidence {score_percent:.1f}%")
            print(f"Bounding box (pixels): left={left:.1f}, top={top:.1f}, right={right:.1f}, bottom={bottom:.1f}")
            print(f"Size: width={width_box:.1f}px, height={height_box:.1f}px")

    # Show image with detections if desired
    if show_image:
        fig, ax = plt.subplots(1)
        ax.imshow(img)

        for score, _, label, rect in apple_detections:
            score_percent = score * 100
            if score_percent < min_score_percent:
                continue
            left, top, right, bottom = rect
            width_box = right - left
            height_box = bottom - top
            rect_patch = patches.Rectangle((left, top), width_box, height_box,
                                           linewidth=2, edgecolor='red', facecolor='none')
            ax.add_patch(rect_patch)
            ax.text(left, top - 10, f"{label}: {score_percent:.1f}%", color='red', fontsize=8, weight='bold')

        plt.title("Apple Detection")
        plt.show()
