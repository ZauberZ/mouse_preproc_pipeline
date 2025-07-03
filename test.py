import ants

atlas=ants.image_read('/media/zzb/data/mouse/template/lr/WHS_0.5_Labels_oc.nii')
img=ants.image_read('/media/zzb/data/mouse/template/lr/canon_T2W_half_rez_oc.nii')
mask_data=atlas.numpy()
mask_data[mask_data>0]=1
atlas[:,:,:]=mask_data
img_=ants.mask_image(img,atlas)
img_.to_file('/media/zzb/data/mouse/template/lr/canon_T2W_brain_half_rez_oc.nii')