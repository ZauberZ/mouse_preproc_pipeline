#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：mouse_preproc_pipeline
@File    ：fMRI_preproc.py
@Author  ：Zauber
@Date    ：2025/3/6 22:45
"""
import ants
from termcolor import colored

def get_mask(SUBJECT_DIR):
    average_tmp = ants.image_read(SUBJECT_DIR + '/average_tmp.nii.gz')
    tmp=ants.image_read('template/mouse_template_0.2mm.nii.gz')
    mask=ants.image_read('template/Brain_mask_0.2mm.nii.gz')
    t=ants.registration(average_tmp,tmp,type_of_transform='SyN',syn_metric='mattes',aff_metric='GC')
    mask_=ants.apply_transforms(average_tmp,mask,t['fwdtransforms'],interpolator='multiLabel')
    mask_.to_file(SUBJECT_DIR+'/mask.nii.gz')
    return mask_

def normalize_toTMP(SUBJECT_DIR):
    print(colored('normalize to template space, please wait...', "red"))
    tmp=ants.image_read('template/ambmc_oc_0.2mm.nii')
    average_tmp=ants.image_read(SUBJECT_DIR+'/average_tmp.nii.gz')
    imgs = ants.image_read(SUBJECT_DIR + '/bold_mc.nii.gz')
    mask=ants.image_read(SUBJECT_DIR + '/mask.nii.gz')
    average_tmp=ants.mask_image(average_tmp,mask)
    t=ants.registration(tmp,average_tmp,type_of_transform='SyN')
    average_tmp_ = ants.apply_transforms(tmp, average_tmp, t['fwdtransforms'], interpolator='bSpline')
    imgs_=ants.apply_transforms(tmp,imgs,t['fwdtransforms'],interpolator='bSpline',imagetype=3)
    average_tmp_.to_file(SUBJECT_DIR+'/average_tmp_norm.nii.gz')
    imgs_.to_file(SUBJECT_DIR+'/bold_mc_norm.nii.gz')
    imgs_s=ants.smooth_image(imgs_,sigma=2,FWHM=True,max_kernel_width=2)
    imgs_s.to_file(SUBJECT_DIR + '/bold_mc_norm_s.nii.gz')
    print(colored('normalize to template space end', "green"))

def meta_copy_4Dto3D(reference,img_data):
    img = ants.from_numpy(img_data)
    img.set_spacing(reference.spacing[0:3])
    img.set_origin(reference.origin[0:3])
    d = reference.direction[0:3, 0:3].copy()
    img.set_direction(d)
    return img
