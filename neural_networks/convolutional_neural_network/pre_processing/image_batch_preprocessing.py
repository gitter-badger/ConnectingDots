import numpy as np
from scipy.misc import imread
from scipy.misc import imresize

from neural_networks.convolutional_neural_network.convnet_keras.convnetskeras.convnets import ALEXNET_IMAGE_SHAPE, \
    VGG_16_IMAGE_SHAPE, VGG_19_IMAGE_SHAPE

IMAGE_RESIZE_DIMENSION_DICT = {
    'alexnet': ALEXNET_IMAGE_SHAPE,
    'vgg_16': VGG_16_IMAGE_SHAPE,
    'vgg_19': VGG_19_IMAGE_SHAPE

}


def preprocess_image_batch(image_paths, network_architecture_used, crop_size=None, color_mode='rgb',
                           out=None):
    """
    Consistent preprocessing of images batches
    :param network_architecture_used:
    :param image_paths: iterable: images to process
    :param crop_size: tuple: crop images if specified
    :param img_size: tuple: resize images if specified
    :param color_mode: Use rgb or change to bgr mode based on type of model you want to use
    :param out: append output to this iterable if specified
    """
    img_list = []
    img_size = get_image_resize_dimension(network_architecture_used)
    for im_path in image_paths:
        img = imread(im_path, mode='RGB')
        if img_size:
            img = imresize(img, img_size)

        img = img.astype('float32')
        # We normalize the colors (in RGB space) with the empirical means on the training set
        img[:, :, 0] -= 123.68
        img[:, :, 1] -= 116.779
        img[:, :, 2] -= 103.939
        # We permute the colors to get them in the BGR order
        if color_mode == 'bgr':
            img[:, :, [0, 1, 2]] = img[:, :, [2, 1, 0]]
        img = img.transpose((2, 0, 1))

        if crop_size:
            img = img[:, (img_size[0] - crop_size[0]) // 2:(img_size[0] + crop_size[0]) // 2
            , (img_size[1] - crop_size[1]) // 2:(img_size[1] + crop_size[1]) // 2]

        img_list.append(img)

    try:
        img_batch = np.stack(img_list, axis=0)
    except:
        raise ValueError('when img_size and crop_size are None, images'
                         ' in image_paths must have the same shapes.')

    if out is not None and hasattr(out, 'append'):
        out.append(img_batch)
    else:
        return img_batch


def get_image_resize_dimension(network_architecture_used):
    return IMAGE_RESIZE_DIMENSION_DICT.get(network_architecture_used)
