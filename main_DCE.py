from utils.dce_pre import pre_dce, normalize_toTMP

# subject path (it must contain MRI bold file, and the file suffix ends with .nii or .nii.gz)
SUBJECT_DIR='/media/zzb/data/mouse/data/dce/'
# The full name of the subject contains a suffix (The file name of MRI dce in SUBJECT_DIR)
# e.g. dce.nii or dce.nii.gz
SUBJECT_NAME='dce.nii'
byMRI=True
MRI='T2w_0.07mm.nii'
template_path='template/WHS/canon_T2W_brain_half_rez_oc.nii'
atlas_path='template/WHS/WHS_0.5_Labels_oc.nii'

def main():
    pre_dce(SUBJECT_DIR,SUBJECT_NAME,byMRI,MRI)
    # normalize_toTMP(SUBJECT_DIR,template_path,atlas_path,byMRI,MRI)
main()