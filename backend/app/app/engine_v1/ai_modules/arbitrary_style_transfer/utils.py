# Utility

import numpy as np

from os import listdir, mkdir, sep
from os.path import join, exists, splitext
from scipy.misc import imread, imsave, imresize


def list_images(directory):
    images = []
    for file in listdir(directory):
        name = file.lower()
        if name.endswith('.png'):
            images.append(join(directory, file))
        elif name.endswith('.jpg'):
            images.append(join(directory, file))
        elif name.endswith('.jpeg'):
            images.append(join(directory, file))
    return images


def get_train_images(paths, resize_len=512, crop_height=256, crop_width=256):
    images = []
    for path in paths:
        image = imread(path, mode='RGB')
        height, width, _ = image.shape

        if height < width:
            new_height = resize_len
            new_width  = int(width * new_height / height)
        else:
            new_width  = resize_len
            new_height = int(height * new_width / width)

        image = imresize(image, [new_height, new_width], interp='nearest')

        # crop the image
        start_h = np.random.choice(new_height - crop_height + 1)
        start_w = np.random.choice(new_width - crop_width + 1)
        image = image[start_h:(start_h + crop_height), start_w:(start_w + crop_width), :]

        images.append(image)

    images = np.stack(images, axis=0)

    return images


def get_images(paths, height=None, width=None):
    if isinstance(paths, str):
        paths = [paths]

    images = []
    for path in paths:
        image = imread(path, mode='RGB')

        if height is not None and width is not None:
            image = imresize(image, [height, width], interp='nearest')

        images.append(image)

    images = np.stack(images, axis=0)

    return images


def save_images(datas, contents_path, styles_path, save_dir, suffix=None):

    assert(len(datas) == len(contents_path) * len(styles_path))

    data_idx = 0
    for content_path in contents_path:
        for style_path in styles_path:
            data = datas[data_idx]
            data_idx += 1
            save_image(data, content_path, style_path, save_dir, suffix)


def save_image(data, content_path, style_path, save_dir, suffix=None):

    if not exists(save_dir):
        mkdir(save_dir)

    if suffix is None:
        suffix = ''

    content_path_name, content_ext = splitext(content_path)
    style_path_name, style_ext = splitext(style_path)

    content_name = content_path_name.split(sep)[-1]
    style_name = style_path_name.split(sep)[-1]
    
    save_path = join(save_dir, '%s-%s%s%s' % 
        (content_name, style_name, suffix, content_ext))

    imsave(save_path, data)

