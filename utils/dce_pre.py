#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：mouse_preproc_pipeline
@File    ：dce_pre.py
@Date    ：2025/7/2 22:43
"""
import ants
import numpy as np
from utils.util import meta_copy_4Dto3D
from termcolor import colored

def pre_dce(SUBJECT_DIR,fname,byMRI,T1w,T2w,step=0):
    print('Start to preproc dce')
    if step == 0:
        img = ants.image_read(SUBJECT_DIR + '/'+fname)
    else:
        img=ants.image_read(SUBJECT_DIR+'/dec_mc.nii.gz')
    print('Motion correction')
    img_mc=ants.motion_correction(img)
    img_mc=img_mc['motion_corrected']
    if byMRI:
        print('Reg by self-individual MRI')
        img_data = img_mc.numpy()
        average_tmp_data = np.mean(img_data[:,:,:,0:5], 3)
        avg=meta_copy_4Dto3D(img_mc,average_tmp_data)
        if T1w is not None:
            print('Correct dce by T1w')
            mri=ants.image_read(SUBJECT_DIR+'/'+T1w)
            t2=ants.image_read(SUBJECT_DIR+'/'+T2w)
            if np.ndim(mri.numpy()) > 3:
                mri_data = mri.numpy()
                mri_avg = np.mean(mri_data, 3)
                mri = meta_copy_4Dto3D(mri, mri_avg)
            if np.ndim(t2.numpy()) > 3:
                t2_data = t2.numpy()
                t2_avg = np.mean(t2_data, 3)
                t2 = meta_copy_4Dto3D(t2, t2_avg)
            tmri=ants.registration(t2,mri,'Similarity',aff_metric='mattes')
            mri = ants.apply_transforms(t2, mri, tmri['fwdtransforms'], 'bSpline')
            mri.to_file(SUBJECT_DIR + '/T1w_aligntoT2w.nii.gz')
        else:
            print('Correct dce by T2w')
            t2 = ants.image_read(SUBJECT_DIR + '/' + T2w)
            mri=t2
        t=ants.registration(mri,avg,'Similarity',aff_metric='mattes')
        t['warpedmovout'].to_file(SUBJECT_DIR+'/avg.nii.gz')
        img_mc_=ants.apply_transforms(mri,img_mc,t['fwdtransforms'],'bSpline',3)

        mtmp=ants.image_read('template/MTMP/mouse_template_0.2mm.nii.gz')
        mask = ants.image_read('template/MTMP/Brain_mask_0.2mm.nii.gz')
        tt = ants.registration(mtmp, t2, 'SyN',reg_iterations=(40, 20, 0))
        mask_=ants.apply_transforms(mri, mask, tt['invtransforms'], 'multiLabel')
        mask_.to_file(SUBJECT_DIR+'/MRI_mask.nii.gz')
    else:
        img_data = img_mc.numpy()
        average_tmp_data = np.mean(img_data[:,:,:,0:5], 3)
        avg=meta_copy_4Dto3D(img_mc,average_tmp_data)
        avg.to_file(SUBJECT_DIR+'/avg.nii.gz')
        img_mc_=img_mc
    img_mc_.to_file(SUBJECT_DIR+'/dce_mc.nii.gz')
    print(colored('DCE preproc end', "green"))

def normalize_toTMP(SUBJECT_DIR,template_path,atlas_path,byMRI,MRI):
    print(colored('Normalize to template space, please wait...', "red"))
    tmp=ants.image_read(template_path)
    atlas = ants.image_read(atlas_path)
    dce=ants.image_read(SUBJECT_DIR+'/dce_mc.nii.gz')
    if byMRI:
        mask=ants.image_read(SUBJECT_DIR+'/MRI_mask.nii.gz')
        img=ants.image_read(SUBJECT_DIR+'/'+MRI)
        img=ants.mask_image(img,mask)
    else:
        img=ants.image_read(SUBJECT_DIR+'/avg.nii.gz')
    t=ants.registration(tmp,img,type_of_transform='SyN')
    img_ = ants.apply_transforms(tmp, img, t['fwdtransforms'], interpolator='bSpline')
    atlas_=ants.apply_transforms(img,atlas,t['invtransforms'],interpolator='multiLabel')
    dce_ = ants.apply_transforms(tmp, dce, t['fwdtransforms'], interpolator='bSpline',imagetype=3)
    atlas_.to_file(SUBJECT_DIR+'/atlas_inDCE.nii.gz')
    img_.to_file(SUBJECT_DIR+'/img_inTMP.nii.gz')
    dce_.to_file(SUBJECT_DIR+'/DCE_inTMP.nii.gz')
    atlas.to_file(SUBJECT_DIR+'/atlas_inTMP.nii.gz')
    print(colored('Normalize to template space end', "green"))