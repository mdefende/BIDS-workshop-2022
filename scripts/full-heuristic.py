import os


def create_key(template, outtype=('nii.gz',), annotation_classes=None):
    if template is None or not template:
        raise ValueError('Template must be a valid format string')
    return template, outtype, annotation_classes


def infotodict(seqinfo):
    """Heuristic evaluator for determining which runs belong where

    allowed template fields - follow python string module:

    item: index within category
    subject: participant id
    seqitem: run number during scanning
    subindex: sub index within group
    """

    # T1w
    t1 = create_key('sub-{subject}/anat/sub-{subject}_T1w')

    # Resting State
    rest = create_key('sub-{subject}/func/sub-{subject}_task-rest_dir-{dir}_run-{item:01d}_bold')
    rest_sbref = create_key('sub-{subject}/func/sub-{subject}_task-rest_dir-{dir}_run-{item:01d}_sbref')

    # Diffusion
    dwi = create_key('sub-{subject}/dwi/sub-{subject}_dir-{dir}_run-{item:01d}_dwi')
    dwi_sbref = create_key('sub-{subject}/dwi/sub-{subject}_dir-{dir}_run-{item:01d}_sbref')

    # Fieldmaps
    fmap = create_key('sub-{subject}/fmap/sub-{subject}_dir-{dir}_run-{item:01d}_epi')

    info = {t1: [], rest: [], rest_sbref: [], dwi: [], dwi_sbref: [], fmap: []}
    last_run = len(seqinfo)

    for s in seqinfo:
        if ('T1w' in s.protocol_name) and ('NORM' in s.image_type):
            info[t1] = [s.series_id]
        if ('REST' in s.protocol_name) and ('AP' in s.protocol_name) and (s.dim4 == 420):
            info[rest].append({'item': s.series_id, 'dir': 'AP'})
        if ('REST' in s.protocol_name) and ('PA' in s.protocol_name) and (s.dim4 == 420):
            info[rest].append({'item': s.series_id, 'dir': 'PA'})
        if ('REST' in s.protocol_name) and ('AP' in s.protocol_name) and (s.dim4 == 1):
            info[rest_sbref].append({'item': s.series_id, 'dir': 'AP'})
        if ('REST' in s.protocol_name) and ('PA' in s.protocol_name) and (s.dim4 == 1):
            info[rest_sbref].append({'item': s.series_id, 'dir': 'PA'})
        if ('dMRI' in s.protocol_name) and ('AP' in s.protocol_name) and (s.dim4 == 100):
            info[dwi].append({'item': s.series_id, 'dir': 'AP'})
        if ('dMRI' in s.protocol_name) and ('AP' in s.protocol_name) and (s.dim4 == 1):
            info[dwi_sbref].append({'item': s.series_id, 'dir': 'AP'})
        if ('SpinEchoFieldMap_AP' in s.protocol_name):
            info[fmap].append({'item': s.series_id, 'dir': 'AP'})
        if ('SpinEchoFieldMap_PA' in s.protocol_name):
            info[fmap].append({'item': s.series_id, 'dir': 'PA'})
    return info
