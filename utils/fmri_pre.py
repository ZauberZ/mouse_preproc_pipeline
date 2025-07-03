#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：mouse_preproc_pipeline
@File    ：fMRI_preproc.py
@Author  ：Zauber
@Date    ：2025/3/6 22:43
"""
import matplotlib.pyplot as plt
import ants
import numpy as np
from termcolor import colored
from utils.util import get_mask


def pre_fmri(SUBJECT_DIR,fname='bold.nii',step=0):
    if step == 0:
        img = ants.image_read(SUBJECT_DIR + '/'+fname)
    else:
        img=ants.image_read(SUBJECT_DIR+'/bold_mc.nii.gz')
    img_data=img.numpy()
    average_tmp_data=np.mean(img_data,3)
    average_tmp=ants.from_numpy(average_tmp_data)
    average_tmp.set_spacing(img.spacing[0:3])
    average_tmp.set_origin(img.origin[0:3])
    d = img.direction[0:3, 0:3].copy()
    average_tmp.set_direction(d)
    if step == 1:
        average_tmp=ants.denoise_image(average_tmp)
        mask=get_mask(SUBJECT_DIR)
        average_tmp=ants.n4_bias_field_correction(average_tmp,mask=mask,shrink_factor=8)
        average_tmp=ants.n4_bias_field_correction(average_tmp,mask=mask, shrink_factor=4)
        average_tmp = ants.n4_bias_field_correction(average_tmp,mask=mask, shrink_factor=2)
    average_tmp.to_file(SUBJECT_DIR+'/average_tmp.nii.gz')

def motion_correction(SUBJECT_DIR,fname='bold.nii',img_name='motion_correction',step=0,isPlot=False):
    print(colored('motion correction, please waite a minute',"red"))
    img_origin_data=None
    if step == 0:
        img = ants.image_read(SUBJECT_DIR+'/'+fname)
    else:
        img = ants.image_read(SUBJECT_DIR + '/bold_mc.nii.gz')
        img_origin=ants.image_read(SUBJECT_DIR+'/'+fname)
        img_origin_data=img_origin.numpy().copy()
    average_tmp = ants.image_read(SUBJECT_DIR+'/average_tmp.nii.gz')
    img_data=img.numpy()
    img_data_=img_data.copy()
    img_data_[:,:,:,:]=0
    n=img_data.shape[3]
    origin_mse=[]
    origin_mse_=[]
    corrected_mse=[]
    frame1st=None
    for i in range(0,n):
        img_iter = ants.from_numpy(img_data[:,:,:,i])
        img_iter.set_spacing(img.spacing[0:3])
        img_iter.set_origin(img.origin[0:3])
        d = img.direction[0:3, 0:3].copy()
        img_iter.set_direction(d)
        t=ants.registration(average_tmp,img_iter,type_of_transform='Rigid',aff_metric='GC')
        img_iter_=ants.apply_transforms(average_tmp,img_iter,t['fwdtransforms'],interpolator='bSpline')
        img_data_[:,:,:,i]=img_iter_.numpy()
        if i==0:
            frame1st = average_tmp
        else:
            c=-ants.image_similarity(frame1st,img_iter,'Correlation')
            c_ = -ants.image_similarity(frame1st, img_iter_, 'Correlation')
            origin_mse.append(c)
            corrected_mse.append(c_)
            if step == 1:
                img_origin_iter = ants.from_numpy(img_origin_data[:, :, :, i])
                img_origin_iter.set_spacing(img.spacing[0:3])
                img_origin_iter.set_origin(img.origin[0:3])
                d = img.direction[0:3, 0:3].copy()
                img_origin_iter.set_direction(d)
                c_origin = -ants.image_similarity(frame1st, img_origin_iter, 'Correlation')
                origin_mse_.append(c_origin)
        print('total: '+str(n)+' n: '+str(i))
    img_=ants.from_numpy(img_data_)
    img_.set_spacing(img.spacing)
    img_.set_origin(img.origin)
    img_.set_direction(img.direction)
    img_.to_file(SUBJECT_DIR+'/bold_mc.nii.gz')
    if isPlot:
        if step == 0:
            plt.plot(origin_mse, label='Origin time-series', color='red')
            plt.plot(corrected_mse, label='The Corrected time-series', color='blue')
        else:
            plt.plot(origin_mse, label='The 1st Corrected time-series', color='red')
            plt.plot(corrected_mse, label='The 2st Corrected time-series', color='blue')
            plt.plot(origin_mse_, label='The orginal time-series', color='green')
        plt.legend()
        plt.grid(True)
        plt.savefig(SUBJECT_DIR+'/'+img_name+'.png', dpi=600)
        plt.show()
    print(colored('motion correction end', "green"))

