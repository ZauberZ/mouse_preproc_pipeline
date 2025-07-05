from utils.dce_pre import pre_dce, normalize_toTMP

# subject path (it must contain MRI dce file, and the file suffix ends with .nii or .nii.gz)
SUBJECT_DIR='/media/zzb/data/mouse/data/dce/'
# The full name of the subject contains a suffix (The file name of MRI dce in SUBJECT_DIR)
# e.g. dce.nii or dce.nii.gz
SUBJECT_NAME='dce.nii'
# Normalize DCE to TMP
isNorm=False
# Reg by self-individual MRI
byMRI=True
# T1w is an optional option. If T1w is not available, please set it to None.
T1w='T1w_0.07mm.nii'
# T2w is a required option.
T2w='T2w_0.07mm.nii'
# You can set brain template to reg
template_path='template/WHS/canon_T2W_brain_half_rez_oc.nii'
atlas_path='template/WHS/WHS_0.5_Labels_oc.nii'


def main():
    pre_dce(SUBJECT_DIR,SUBJECT_NAME,byMRI,T1w,T2w)
    normalize_toTMP(SUBJECT_DIR,template_path,atlas_path,byMRI,T2w)
main()