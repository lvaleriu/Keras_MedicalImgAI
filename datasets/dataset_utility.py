import os

import cv2
import numpy as np


def pos_count(subset_series, class_names):
    ret_dict = dict()
    one_hot_labels = np.array(subset_series["One_Hot_Labels"].tolist())
    for i, c in enumerate(class_names):
        ret_dict[c] = np.int(np.sum(one_hot_labels[:, i]))
    print(f"{ret_dict}")
    return ret_dict


def batch_generator(image_filenames, labels, image_dir, img_dim=256, scale=1. / 255, colormode='grayscale'):
    if colormode == 'grayscale':
        inputs = np.array(
            image_filenames.apply(lambda x: load_image(x, image_dir, img_dim=img_dim, scale=scale)).tolist())[:, :, :,
                 np.newaxis]
    else:
        inputs = np.array(
            image_filenames.apply(lambda x: load_image(x, image_dir, img_dim=img_dim, scale=scale)).tolist())
    targets = np.array(labels)
    return (inputs, targets)


def load_image(image_name, image_dir, img_dim=256, scale=1. / 255, colormode='grayscale', verbose=2):
    image_file = image_dir + "/" + image_name;
    if not os.path.isfile(image_file):
        raise Exception(f"{image_file} not found")
    if verbose > 1:
        print(f"Load image from {image_file}")
    image = cv2.imread(image_file, 0)[:, :, np.newaxis]
    image = cv2.resize(image, (img_dim, img_dim))
    return image * scale


def label2vec(label, class_names):
    vec = np.zeros(len(class_names))
    if label == "No Finding":
        return vec
    labels = label.split("|")
    for l in labels:
        vec[class_names.index(l)] = 1
    return vec