#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：mouse_preproc_pipeline
@File    ：fMRI_preproc.py
@Author  ：Zauber
@Date    ：2025/3/28 17:03
"""
import numpy as np
import ants
import pandas as pd
import matplotlib.pyplot as plt

def calc_bold_value_byatlas(SUBJECT_DIR,SUBJECT_NAME,atlas_fn='mask_oc_0.2mm',isPlot=False,region_name='1'):
    atlas=ants.image_read('template/'+atlas_fn+'.nii')
    bold=ants.image_read(SUBJECT_DIR+'/'+SUBJECT_NAME+'.nii.gz')
    bold_data=bold.numpy()
    atlas_data=atlas.numpy()
    regions=np.unique(atlas_data)
    regions = regions[regions > 0]
    regions_name = np.astype(regions, int)
    regions_name=np.astype(regions_name,str)
    data = np.zeros((bold_data.shape[3], len(regions)))
    df=pd.DataFrame(data,columns=regions_name)
    for i in range(len(regions)):
        atlas_data_ = atlas_data.copy()
        nonz = atlas_data_ == regions[i]
        for frame_index in range(bold_data.shape[3]):
            frame=bold_data[:,:,:,frame_index]
            m=np.mean(frame,where=nonz)
            df.at[frame_index, str(regions_name[i])] = m
    df.to_csv(SUBJECT_DIR+'/'+SUBJECT_NAME+'_'+atlas_fn+'.csv')
    if isPlot:
        plt.plot(df[str(region_name)].to_list(), label='region_name: '+str(region_name), color='red')
        plt.legend()
        plt.grid(True)
        plt.savefig(SUBJECT_DIR + '/plot_bold.png', dpi=600)
        plt.show()

def calc_volume_byMask(SUBJECT_DIR,MASK_NAME):
    mask=ants.image_read(SUBJECT_DIR+'/'+MASK_NAME)
    units=mask.spacing
    mask_data=mask.numpy()
    cubes_num=mask_data[mask_data>0]
    cube_volume=units[0]*units[1]*units[2]
    volume=cube_volume*len(cubes_num)
    return volume


