#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import numpy as np
from visual import *
from nite2 import *
import cv2

g_visibleUsers = 10*[False]
g_skeletonStates = 10*[SKELETON_NONE]

_bone_ids4 = [
    # Torso
    [JOINT_HEAD, JOINT_NECK]]


_bone_ids3 = [
    # Torso
    [JOINT_HEAD, JOINT_NECK],
    [JOINT_NECK, JOINT_LEFT_SHOULDER],
    [JOINT_NECK, JOINT_RIGHT_SHOULDER],
    [JOINT_NECK, JOINT_TORSO],
    [JOINT_TORSO, JOINT_LEFT_HIP],
    [JOINT_TORSO, JOINT_RIGHT_HIP],
    # Braco direito
    [JOINT_RIGHT_SHOULDER, JOINT_RIGHT_ELBOW],
    [JOINT_RIGHT_ELBOW, JOINT_RIGHT_HAND],
    # Braco esquerdo
    [JOINT_LEFT_SHOULDER, JOINT_LEFT_ELBOW],
    [JOINT_LEFT_ELBOW, JOINT_LEFT_HAND],
    # Perna direita
    [JOINT_RIGHT_HIP, JOINT_RIGHT_KNEE],
    [JOINT_RIGHT_KNEE, JOINT_RIGHT_FOOT],
    # Perna esquerda
    [JOINT_LEFT_HIP, JOINT_LEFT_KNEE],
    [JOINT_LEFT_KNEE, JOINT_LEFT_FOOT]]


def update_user_state(user, ts):
    if user.isNew():
        print 'User:', user.id, ' - New'
    elif user.isVisible() and (not g_visibleUsers[user.id]):
        print 'User:', user.id, ' - Visible'
    elif (not user.isVisible()) and g_visibleUsers[user.id]:
        print 'User:', user.id, ' - Out of Scene'
    elif user.isLost():
        print 'User:', user.id, ' - Lost'

    g_visibleUsers[user.id] = user.isVisible()

    if g_skeletonStates[user.id] != user.skeleton.state:
        state = g_skeletonStates[user.id] = user.skeleton.state
        if state == SKELETON_NONE:
            print 'User:', user.id, ' - Stopped tracking'
        elif state == SKELETON_CALIBRATING:
            print 'User:', user.id, ' - Calibrating...'
        elif state == SKELETON_TRACKED:
            print 'User:', user.id, ' - Tracking!'
        elif state in [SKELETON_CALIBRATION_ERROR_NOT_IN_POSE, 
                       SKELETON_CALIBRATION_ERROR_HANDS,
                       SKELETON_CALIBRATION_ERROR_LEGS,
                       SKELETON_CALIBRATION_ERROR_HEAD,
                       SKELETON_CALIBRATION_ERROR_TORSO]:
            print 'User:', user.id, ' - Calibration Failed... :-|'

def draw_user(skeleton,listaIndices,listaCilindros):
    for bone, bone_id in zip(listaCilindros, listaIndices):
        p1 = skeleton.getJoint(bone_id[0])
        p2 = skeleton.getJoint(bone_id[1])

        bone.pos = (p1.position.x, p1.position.y, p1.position.z)
        bone.axis = (p2.position.x - p1.position.x,
                     p2.position.y - p1.position.y,
                     p2.position.z - p1.position.z)


def draw_sensor(f):
    """Draw 3D model of the Kinect sensor.

    Draw the sensor in the given (and returned) VPython frame f, with
    the depth sensor frame aligned with f.
    """
    box(frame=f, pos=(0, 0, 0), length=0.2794, height=0.0381, width=0.0635,
        color=color.blue)
    cylinder(frame=f, pos=(0, -0.05715, 0), axis=(0, 0.0127, 0), radius=0.0381,
             color=color.blue)
    cone(frame=f, pos=(0, -0.04445, 0), axis=(0, 0.01905, 0), radius=0.0381,
         color=color.blue)
    cylinder(frame=f, pos=(0, -0.05715, 0), axis=(0, 0.0381, 0), radius=0.0127,
             color=color.blue)
    cylinder(frame=f, pos=(-0.0635, 0, 0.03175), axis=(0, 0, 0.003),
             radius=0.00635, color=color.red)
    cylinder(frame=f, pos=(-0.0127, 0, 0.03175), axis=(0, 0, 0.003),
             radius=0.00635, color=color.red)
    cylinder(frame=f, pos=(0.0127, 0, 0.03175), axis=(0, 0, 0.003),
             radius=0.00635, color=color.red)
    text(frame=f, text='KINECT', pos=(0.06985, -0.00635, 0.03175),
         align='center', height=0.0127, depth=0.003)
    # colocando eixos
    # cylinder(frame=f, pos=(0,0,0), axis=(1,0,0), radius=0.001,color=color.red)
    # cylinder(frame=f, pos=(0,0,0), axis=(0,1,0), radius=0.001,color=color.green)
    # cylinder(frame=f, pos=(0,0,0), axis=(0,0,1), radius=0.001,color=color.blue)

    return f

if __name__ == "__main__":
    # criando ambiente
    display(title='Nit2',
            x=0, y=0, width=1200, height=700,
            center=(0, 0, 0), background=(0, 0, 0))

    frameVisual = frame()
    draw_sensor(frameVisual)

    # definindo lista de ossos
    bones = [cylinder(frame=frameVisual, radius=0.02, color=color.yellow)
                  for bone in _bone_ids3]

    rc = OpenNI.initialize()
    if rc != OPENNI_STATUS_OK:
        raise Exception('OpenNI initialize error: ' + str(rc))

    rc = NiTE.initialize()
    if rc != NITE_STATUS_OK:
        raise Exception('NiTE initialize error: ' + str(rc))

    dev = Device()
    rc = dev.open()
    if rc != OPENNI_STATUS_OK:
        raise Exception('device open error: ' + str(rc))

    if dev.isImageRegistrationModeSupported(IMAGE_REGISTRATION_DEPTH_TO_COLOR):
        dev.setImageRegistrationMode(IMAGE_REGISTRATION_DEPTH_TO_COLOR)

    col = VideoStream()
    dep = VideoStream()
    
    rc = col.create(dev, SENSOR_COLOR)
    if rc != OPENNI_STATUS_OK:
        raise Exception('color stream create error: ' + str(rc))

    rc = dep.create(dev, SENSOR_DEPTH)
    if rc != OPENNI_STATUS_OK:
        raise Exception('depth stream create error: ' + str(rc))

    rc = col.start()
    if rc != OPENNI_STATUS_OK:
        raise Exception('color stream start error: ' + str(rc))

    rc = dep.start()
    if rc != OPENNI_STATUS_OK:
        raise Exception('depth stream start error: ', + str(rc))
    
    ut = UserTracker()
    
    rc = ut.create()
    if rc != NITE_STATUS_OK:
        raise Exception('error creating user tracker: ' + str(rc))

    print 'Start moving around to get detected...'
    print '(PSI pose may be required for skeleton calibration, depending on the configuration)'

    flag = 0
    ang  = 0
    pos = 0
    try:
        while True:
            rc, color = col.readFrame()
            if rc != OPENNI_STATUS_OK:
                raise Exception('error reading color frame: ' + str(rc))

            rc, depth = dep.readFrame()
            if rc != OPENNI_STATUS_OK:
                raise Exception('error reading depth frame: ' + str(rc))

            rc, frame = ut.readFrame()
            if rc != OPENNI_STATUS_OK:
                raise Exception('read frame error: ' + str(rc))
                
            users = frame.users
            updateVisual = False

            for u in users:
                update_user_state(u, frame.timestamp)
                if u.isNew():
                    ut.startSkeletonTracking(u.id)
                elif u.skeleton.state == SKELETON_TRACKED:
                    #print "RECEBENDO DADOS ESQUELETO !!!!!!!"
                    updateVisual = True


                    for bone, bone_id in zip(bones, _bone_ids3):
                        p1 = u.skeleton.getJoint(bone_id[0])
                        p2 = u.skeleton.getJoint(bone_id[1])

                        bone.pos = [float(p1.position.x),
                                    float(p1.position.y),
                                    float(p1.position.z)]

                        bone.axis = [float(p2.position.x - p1.position.x),
                                     float(p2.position.y - p1.position.y),
                                     float(p2.position.z - p1.position.z)]
                        # convertendo de mm para metro

                        bone.pos = bone.pos/1000
                        bone.axis = bone.axis/1000

                        #bone.radius = 0.1
                    #flag = 1

            rate(30)
            frameVisual.visible = updateVisual

            #k = cv2.waitKey(10)
            #if k == 27:
            #    break
                    
    finally:
        ut.destroy()
        col.destroy()
        dep.destroy()
        dev.close()
        OpenNI.shutdown()
        NiTE.shutdown()
        print 'shutdown'
        
