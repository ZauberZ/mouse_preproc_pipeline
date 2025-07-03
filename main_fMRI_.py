from utils.fmri_pre import pre_fmri, motion_correction
from utils.util import normalize_toTMP

# subject path (it must contain MRI bold file, and the file suffix ends with .nii or .nii.gz)
SUBJECT_DIR='/home/zzb/PycharmProjects/mouse_preproc_pipeline/test/'
# The full name of the subject contains a suffix (The file name of MRI bold in SUBJECT_DIR)
# e.g. bold.nii or bold.nii.gz
SUBJECT_NAME='bold.nii'


def main():
    # #iter 1
    pre_fmri(SUBJECT_DIR,SUBJECT_NAME)
    # motion_correction(SUBJECT_DIR,SUBJECT_NAME,'motion_correction_iter1',isPlot=True)
    # # #iter 2
    # pre_fmri(SUBJECT_DIR, 'bold_mc.nii.gz')
    motion_correction(SUBJECT_DIR, 'bold_mc.nii.gz','motion_correction_iter2',0, isPlot=True)
    # # #motion correction end
    # pre_fmri(SUBJECT_DIR,step=1)
    normalize_toTMP(SUBJECT_DIR)
main()