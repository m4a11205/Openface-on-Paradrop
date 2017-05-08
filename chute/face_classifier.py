#!/usr/bin/env python2

import time

start = time.time()

import argparse
import cv2
import os
import pickle

from operator import itemgetter

import numpy as np
np.set_printoptions(precision=2)
import pandas as pd

import openface

from sklearn.pipeline import Pipeline
from sklearn.lda import LDA
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
from sklearn.grid_search import GridSearchCV
from sklearn.mixture import GMM
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB

clfChoices = [
    'LinearSvm',
    'RadialSvm',
    'GaussianNB',
    'Forest',
    'Logic',
    ]


def getRep(imgPath, args, align, net, multiple):
    start = time.time()
    bgrImg = cv2.imread(imgPath)
    if bgrImg is None:
        raise Exception("Unable to load image: {}".format(imgPath))

    rgbImg = cv2.cvtColor(bgrImg, cv2.COLOR_BGR2RGB)

    start = time.time()

    if multiple:
        bbs = align.getAllFaceBoundingBoxes(rgbImg)
    else:
        bb1 = align.getLargestFaceBoundingBox(rgbImg)
        bbs = [bb1]
    if len(bbs) == 0 or (not multiple and bb1 is None):
        raise Exception("Unable to find a face: {}".format(imgPath))

    reps = []
    for bb in bbs:
        start = time.time()
        alignedFace = align.align(
            args.imgDim,
            rgbImg,
            bb,
            landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)
        if alignedFace is None:
            raise Exception("Unable to align image: {}".format(imgPath))

        start = time.time()
        rep = net.forward(alignedFace)
        reps.append((bb.center().x, rep))

    sreps = sorted(reps, key=lambda x: x[0])
    return sreps


def infer(args, align, net, multiple=False):
    scores = []
    people = []

    with open(os.path.join(args.classifierModel, "classifier.pkl"), 'r') as f:
        (le, clf) = pickle.load(f)

    for img in args.imgs:
        print("\n=== {} ===".format(img))

        try:
            reps = getRep(img, args, align, net, multiple)

            if len(reps) > 1:
                print("List of faces in image from left to right")

            for r in reps:
                rep = r[1].reshape(1, -1)
                bbx = r[0]
                start = time.time()
                predictions = clf.predict_proba(rep).ravel()
                maxI = np.argmax(predictions)
                person = le.inverse_transform(maxI)
                confidence = predictions[maxI]

                if(confidence < 0.5 ):
                    person = 'Unknown'
                    confidence = 100

                if multiple:
                    print("Predict {} @ x={} with {:.2f} confidence.".format(person, bbx, confidence))
                else:
                    scores.append(confidence)
                    people.append(person)
                    print("Predict {} with {:.2f} confidence.".format(person, confidence))
                    return scores, people

                if isinstance(clf, GMM):
                    dist = np.linalg.norm(rep - clf.means_[maxI])
                    print("  + Distance from the mean: {}".format(dist))

        except Exception as e:
            print('!! Warning: %s' % str(e))
            return scores, people


def inferMulti(args, align, net):
    scores = []
    people = []
    threshold = -1;
    votes = {}

    for clfChoice in clfChoices:
        print "\n==============="
        print "Using the classifier: " + clfChoice

        with open(os.path.join(args.classifierModel, clfChoice + ".pkl"), 'r') as f_clf:
            (le, clf) = pickle.load(f_clf)

        for img in args.imgs:
            try:
                reps = getRep(img, args, align, net, False)
                rep = reps[0][1].reshape(1, -1)
            except Exception as e:
                print('!! Warning: %s' % str(e))
                return scores, people

            predictions = clf.predict_proba(rep).ravel()
            maxI = np.argmax(predictions)
            person = le.inverse_transform(maxI)
            confidence = predictions[maxI]

            print person, confidence

            if clfChoice == 'LinearSvm':
                threshold = 0.45
            elif clfChoice == 'RadialSvm':  # Radial Basis Function kernel
                threshold = 0.4
            elif clfChoice == 'GaussianNB':
                threshold = 0.9
            elif clfChoice == 'Forest':
                threshold = 0.55
            elif clfChoice == 'Logic':
                threshold = 0.5

            if(confidence < threshold ):
                person = 'Unknown'

            cnt = votes.get(person)
            if(cnt is None):
                votes[person] = 1
            else:
                votes[person] = cnt + 1

    # get majority vote
    maxNum = -1;
    maxName= None;
    for name, num in votes.iteritems():
        if (num > maxNum):
            maxNum = num
            maxName = name

    print maxName, maxNum

    if(maxNum < (len(clfChoices)+1)/2):
        maxName = 'Unknown'
        maxNum  = len(clfChoices) - maxNum

    scores.append( float (maxNum)/ len(clfChoices))
    people.append(maxName)

    print votes
    return scores, people
