#!/usr/bin/env python3

import numpy
import math
import time
import skimage.io
import os.path
import pickle
import torch

from app.engine_v1 import app_config, logger

from . import get_attrs
from . import model_cpu


def center_crop(X, crop):
    '''X is N x H x W x 3'''
    h1 = int(math.ceil((X.shape[1]-crop)/2))
    w1 = int(math.ceil((X.shape[2]-crop)/2))
    return X[:, h1:h1+crop, w1:w1+crop, :]


class FaceModel:
    def __init__(self, modelfile='model.t7'):
        '''
        This model takes a 160x160 input which is a single face aligned to
        self.celeba_template (which is a set of 68 dlib landmarks). Call
        preprocess() then forward() to get a 1024-dim feature vector. Then
        call predict_attributes() on the features to get 40 attribute
        decision values.
        '''
        self.model = model_cpu.model_cpu
        self.model.load_state_dict(torch.load(os.path.join(
            app_config.MODEL_DIR, 'deep_feat_interp/model_cpu.pth'), map_location="cuda:0"))
        self.model.eval()  # set model to test mode
        self.model.cuda()
        self.meanstd = {'mean': numpy.array(
            [0.485, 0.456, 0.406]), 'std': numpy.array([0.229, 0.224, 0.225])}
        self.celeba_template = numpy.load(os.path.join(
            app_config.MODEL_DIR, 'deep_feat_interp/celeba_dlib_template.npz'))['template']
        self.clf = {k: pickle.load(open(os.path.join(
            app_config.MODEL_DIR, 'deep_feat_interp/classifiers/{}.pkl'.format(k)), 'rb'), encoding='iso-8859-1') for k in get_attrs.fields}
        self.fields = tuple(get_attrs.fields)

    def preprocess(self, X):
        '''X is an N x H x W x 3 set of images in the range [0, 1].'''
        X = X-self.meanstd['mean']
        X = X/self.meanstd['std']
        X = center_crop(X, 160)
        return X

    def forward(self, X):
        '''X is an N x H x W x 3 set of images'''
        thX = torch.from_numpy(X.transpose(0, 3, 1, 2))
        thX = thX.type(torch.FloatTensor) # 转Float
        cuthX = thX.cuda() # 转cuda
        assert torch.typename(cuthX) in torch.backends.cudnn._typemap
        thY = self.model.forward(torch.autograd.Variable(cuthX))
        Y = thY.cpu().data.numpy()
        return Y

    def predict_attributes(self, Y):
        '''Returns N x K decision values. K is |self.fields|.'''
        scores = numpy.array([self.clf[k].decision_function(Y)
                              for k in self.fields]).T
        return scores


__doc__ = '''
Command-line tools:

th extract_features.lua -data IMAGEDIR -save OUTPUTDIR
python get_attrs.py results FIELDNAME
'''


if __name__ == '__main__':
    fm = FaceModel()

    import alignface
    face_d, face_p = alignface.load_face_detector(predictor_path=os.path.join(
            app_config.MODEL_DIR, 'deep_feat_interp/shape_predictor_68_face_landmarks.dat'))
    ipath = '../../images/input.png'
    M, X, revmask, original, loss = alignface.fit_face(
        ipath, face_d, face_p, template=fm.celeba_template, image_dims=[160, 160], twoscale=False)
    # skimage.io.imsave('zzz.png',X)
    X = numpy.expand_dims(X, 0)
    X = fm.preprocess(X)
    print('X', X.shape, X.min(), X.mean(), X.max())

    # compare against Geoff's code
    import csv
    f = csv.reader(open('results/features.csv'))
    for i in range(18):
        data = next(f)

    F = numpy.expand_dims(numpy.array([float(x) for x in data[1:]]), 0)

    for i in range(2):
        t0 = time.time()
        Y = fm.forward(X)
        print(F[0, 0], Y[0, 0], numpy.allclose(
            F, Y, rtol=1e-4, atol=1e-4), time.time()-t0)

    scores = fm.predict_attributes(Y)
    #probabilities=numpy.array([clf[k].predict_proba(Y) for k in get_attrs.fields]).T

    for x in scores:
        print(', '.join(['{} ({})'.format(k, x[i]) for i, k in enumerate(fm.fields) if x[i] > 0]))

    for x in scores:
        print(', '.join(['{} ({})'.format(k, x[i]) for i, k in enumerate(fm.fields) if x[i] <= 0]))
