import ants
import numpy as np
from utils.util import meta_copy_4Dto3D
from termcolor import colored

def pre_dce(SUBJECT_DIR,fname,byMRI,MRI,step=0):
    if step == 0:
        img = ants.image_read(SUBJECT_DIR + '/'+fname)
    else:
        img=ants.image_read(SUBJECT_DIR+'/bold_mc.nii.gz')
    img_mc=ants.motion_correction(img)
    img_mc=img_mc['motion_corrected']
    if byMRI:
        img_data = img_mc.numpy()
        average_tmp_data = np.mean(img_data[:,:,:,0:5], 3)
        avg=meta_copy_4Dto3D(img_mc,average_tmp_data)
        mri=ants.image_read(SUBJECT_DIR+'/'+MRI)
        mtmp=ants.image_read('template/MTMP/mouse_template_0.2mm.nii.gz')
        mask = ants.image_read('template/MTMP/Brain_mask_0.2mm.nii.gz')
        tt = ants.registration(mtmp, mri, 'SyN')
        mask_=ants.apply_transforms(mri, mask, tt['invtransforms'], 'multiLabel')
        mask_.to_file(SUBJECT_DIR+'/MRI_mask.nii.gz')
        t=ants.registration(mri,avg,'Similarity')
        t['warpedmovout'].to_file(SUBJECT_DIR+'/avg.nii.gz')
        img_mc_=ants.apply_transforms(mri,img_mc,t['fwdtransforms'],'bSpline',3)
    else:
        img_mc_=img_mc
    img_mc_.to_file(SUBJECT_DIR+'/dce_mc.nii.gz')

def normalize_toTMP(SUBJECT_DIR,template_path,atlas_path,byMRI,MRI,MRI_mask):
    print(colored('normalize to template space, please wait...', "red"))
    tmp=ants.image_read(template_path)
    atlas = ants.image_read(atlas_path)
    if byMRI:
        mask=ants.image_read(SUBJECT_DIR+'/MRI_mask.nii.gz')
        img=ants.image_read(SUBJECT_DIR+'/'+MRI)
        img=ants.mask_image(img,mask)
    else:
        img=ants.image_read(SUBJECT_DIR+'/avg.nii.gz')
    t=ants.registration(tmp,img,type_of_transform='SyN')
    img_ = ants.apply_transforms(tmp, img, t['fwdtransforms'], interpolator='bSpline')
    atlas_=ants.apply_transforms(img,atlas,t['invtransforms'],interpolator='multiLabel')
    atlas_.to_file(SUBJECT_DIR+'/atlas.nii.gz')
    img_.to_file(SUBJECT_DIR+'/img_inTMP.nii.gz')
    print(colored('normalize to template space end', "green"))