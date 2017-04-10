#!/usr/bin/python

import sys, math, os, string, time, argparse, json, subprocess
import httplib
import base64
import StringIO
import thread
from flask import Flask
from flask import request
import openface
import face_classifier
import seccam

try:
    import PIL
    from PIL import Image, ImageChops
except Exception as e:
    print('No PIL, please install "python-imaging-library" if on OpenWrt')
    sys.exit(1)

fileDir = os.path.dirname(os.path.realpath(__file__))
modelDir = '/root/openface/models'
dlibModelDir = os.path.join(modelDir, 'dlib')
openfaceModelDir = os.path.join(modelDir, 'openface')

timeflt = lambda: time.time()

THRESH_0 = 20.0
THRESH_1 = 40.0
THRESH_2 = 60.0

#'''

def setupArgParse():
    parser = argparse.ArgumentParser(description='smarthouse security suite')
    parser.add_argument('-calibrate', help='Temporary mode to help calibrate the thresholds', action='store_true')
    parser.add_argument('-m_sec', help='How much time to wait between motion images', type=float, default=2.0)
    parser.add_argument('-m_sensitivity', help='How sensitive the motion capture should be, 0=very, 1=somewhat, 2=not very', type=int, default=0)

    parser.add_argument(
        '--dlibFacePredictor',
        type=str,
        help="Path to dlib's face predictor.",
        default=os.path.join(
            dlibModelDir,
            "shape_predictor_68_face_landmarks.dat"))
    parser.add_argument(
        '--networkModel',
        type=str,
        help="Path to Torch network model.",
        default=os.path.join(
            openfaceModelDir,
            'nn4.small2.v1.t7'))
    parser.add_argument('--imgDim', type=int,
                        help="Default image dimension.", default=96)
    parser.add_argument('--cuda', action='store_true')
    parser.add_argument('--verbose', action='store_true')

    subparsers = parser.add_subparsers(dest='mode', help="Mode")
    trainParser = subparsers.add_parser('train',
                                        help="Train a new classifier.")
    trainParser.add_argument('--ldaDim', type=int, default=-1)
    trainParser.add_argument(
        '--classifier',
        type=str,
        choices=[
            'LinearSvm',
            'GridSearchSvm',
            'GMM',
            'RadialSvm',
            'DecisionTree',
            'GaussianNB',
            'DBN'],
        help='The type of classifier to use.',
        default='LinearSvm')
    trainParser.add_argument(
        'workDir',
        type=str,
        help="The input work directory containing 'reps.csv' and 'labels.csv'. Obtained from aligning a directory with 'align-dlib' and getting the representations with 'batch-represent'.")

    inferParser = subparsers.add_parser(
        'infer', help='Predict who an image contains from a trained classifier.')
    inferParser.add_argument(
        'classifierModel',
        type=str,
        help='The Python pickle representing the classifier. This is NOT the Torch network model, which can be set with --networkModel.')
    inferParser.add_argument('imgs', type=str, nargs='+',
                             help="Input image.")
    inferParser.add_argument('--multi', help="Infer multiple faces in image",
                                 action="store_true")

    return parser


if(__name__ == "__main__"):
    print("In main\n")

    p = setupArgParse()
    args = p.parse_args()

    m_sec = args.m_sec
    m_save = '/var/www/html/motionLog/motion-'

    print("Welcom to Smart House!!\n")

    if(m_sec < 1.0):
        print('** For the workshop, please do not use lower than 1.0 for m_sec')
        exit()

    #Face recognition setup
    align = openface.AlignDlib(args.dlibFacePredictor)
    net = openface.TorchNeuralNet(args.networkModel, imgDim=args.imgDim, cuda=args.cuda)


    # Get camera IP
    camIP = seccam.getCameraIP(m_sec)
    print("Found camIP %s" % camIP)

    # Run camera app
    try:
       thread.start_new_thread( seccam.run_app, (camIP, m_save, args, align, net) )
    except:
       print "Error: unable to start seccam.run_app thread"

    #while(True):
    #   pass
    seccam.surveillance(camIP, args, m_save)
