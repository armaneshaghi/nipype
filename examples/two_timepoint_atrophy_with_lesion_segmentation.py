##placeholders are as follows, note there is no lesion mask because we generate it:
##{subject_id_to_replace}
##{fu1_t1_nii_gz}
##{fu1_t2_nii_gz}
##{baseline_t1_nii_gz}
##{baseline_t2_nii_gz}

import os
from nipype.interfaces.fsl import FLIRT
from nipype.interfaces.fsl import BET
from nipype.interfaces.fsl import ApplyXfm
from nipype.interfaces.ants import N4BiasFieldCorrection
from nipype import SelectFiles
from nipype.interfaces.fsl import UnaryMaths
from nipype.interfaces.fsl.utils import lesion_filling
from nipype.interfaces.utility import Function
from nipype.interfaces.freesurfer.utils import mri_robust_template
from nipype.interfaces.nmr.utils import steps
from nipype.interfaces.nmr.utils import gif
import nipype.pipeline.engine as pe
import nipype.interfaces.io as nio
import nipype.interfaces.utility as util
from nipype.interfaces.nmr.utils import segmentLesion

subject_list = ['{subject_id_to_replace}']
workflow = pe.Workflow(name = 'second_wave')
workflow.base_dir = '/cluster/project0/MS_LATA/fourd/working/nipype'
infosource = pe.Node(interface = util.IdentityInterface(fields=['subject_id']), 
                                                          name = "infosource")
infosource.iterables = ('subject_id', subject_list)

templates = {{
            "baseline_t1" : '/cluster/project0/MS_LATA/fourd/patients/{{subject_id}}/{baseline_t1_nii_gz}',
            "baseline_t2" : '/cluster/project0/MS_LATA/fourd/patients/{{subject_id}}/{baseline_t2_nii_gz}',
            "fu1_t1" :  '/cluster/project0/MS_LATA/fourd/patients/{{subject_id}}/{fu1_t1_nii_gz}' ,
            "fu1_t2" : '/cluster/project0/MS_LATA/fourd/patients/{{subject_id}}/{fu1_t2_nii_gz}'
             }}

file_selector = pe.Node( SelectFiles(templates), "selectfiles") 

segment_lesion_baseline = pe.Node(name=  'segment_lesion_baseline' , interface = segmentLesion())
segment_lesion_baseline.inputs.flair_lesion = 'flair_lesion.nii.gz'

segment_lesion_fu1 = pe.Node(name=  'segment_lesion_fu1' , interface = segmentLesion())
segment_lesion_fu1.inputs.flair_lesion = 'flair_lesion.nii.gz'

bet_baseline = pe.Node(name = 'bet_baseline',
                       interface = BET())
bet_baseline.inputs.mask = True

bet_fu1 = pe.Node(name = 'bet_fu1', 
                     interface = BET() )
bet_fu1.inputs.mask = True

n4_baseline = pe.Node(name = 'n4_baseline', interface = N4BiasFieldCorrection())
n4_fu1 = pe.Node(name = 'n4_fu1', interface = N4BiasFieldCorrection() )
n4_baseline.inputs.dimension = 3
n4_fu1.inputs.dimension = 3
regt2t1_baseline = pe.Node(interface = FLIRT(), name = 't2t1_baseline')
regt2t1_fu1 = pe.Node(interface = FLIRT(), name = 't2t1_fu1')
regt2maskt1_baseline = pe.Node(interface = ApplyXfm(), 
                              name = 't2maskt1_baseline')
regt2maskt1_baseline.inputs.apply_xfm = True

regt2maskt1_fu1 = pe.Node(interface = ApplyXfm(),
                             name = 't2maskt1_fu1')
regt2maskt1_fu1.inputs.apply_xfm = True

binarise_baseline = pe.Node(interface = UnaryMaths(),
                           name = 'binarise_baseline')
binarise_baseline.inputs.operation = 'bin'

binarise_fu1 = pe.Node(interface = UnaryMaths(),
                           name = 'binarise_fu1')

binarise_fu1.inputs.operation = 'bin'
lesion_filler_baseline = pe.Node(interface = lesion_filling(), 
                      name = 'lesion_filler_baseline')
lesion_filler_fu1 = pe.Node(interface = lesion_filling(),
                               name = 'lesion_filler_fu1')
def lister(volume_baseline, volume_fu1):
    return [volume_baseline, volume_fu1]
lister_node = pe.Node(name = 'lister_node' , 
                     interface = Function(input_names = ['volume_baseline', 
                                                        'volume_fu1'],
                                         output_names = ['volume_list'],
                                      function = lister))
robust_template_maker = pe.Node(interface = mri_robust_template(),
                               name = 'mri_robust_template_maker'
                               )
robust_template_maker.inputs.template = 'within_sub.nii.gz'
robust_template_maker.inputs.moved_images = ['moved2template_baseline.nii.gz',
                                            'moved2template_fu1.nii.gz']
def return_baseline(volume_list):
    return volume_list[0]

def return_fu1(volume_list):
    return volume_list[1]
robust_output_baseline_node = pe.Node(name = 'robust_output_baseline', 
                     interface = Function(input_names = ['volume_list'],
                                          output_names = ['volume_baseline'],
                                          function = return_baseline
                                         ))
robust_output_fu1_node = pe.Node(name = 'robust_output_fu1', 
                     interface = Function(input_names = ['volume_list'],
                                          output_names = ['volume_fu1'],
                                          function = return_fu1
                                         ))
gif_baseline = pe.Node(interface = gif(),
                      name = 'gif_baseline')
gif_baseline.inputs.output_dir = 'gif_output'
gif_fu1 = pe.Node(interface = gif(),
                     name = 'gif_fu1')
gif_fu1.inputs.output_dir = 'gif_output'
brain_steps_baseline = pe.Node(interface = steps(),
                     name = 'brain_steps_baseline')
brain_steps_fu1 = pe.Node(interface =  steps(),
                              name = 'brain_steps_fu1')
brain_steps_baseline.inputs.steps_mask = 'brain_steps_baseline_mask.nii.gz'
brain_steps_fu1.inputs.steps_mask = 'brain_steps_fu1_mask.nii.gz'

#data sink to conserve within-subject template otherwise it is deleted
datasink = pe.Node(nio.DataSink(), name='sinker')
datasink.inputs.base_directory = '/cluster/project0/MS_LATA/fourd/working/nipype/second_wave/'
workflow.connect(infosource, 'subject_id', datasink, 'container')
workflow.connect(robust_template_maker, 'template', datasink, 'within_subject_template')

#note we are pretending t2 = flair, just to make less changes
workflow.connect([
                  (infosource, file_selector,
                   [('subject_id','subject_id')]
                  )
                 ,
                (file_selector, bet_baseline,
                  [('baseline_t1', 'in_file' )]
                 ),
                 (file_selector, bet_fu1,
                 [( 'fu1_t1', 'in_file' )]
                 ),
                 ( file_selector, segment_lesion_baseline,
                  [( 'baseline_t2', 'flair'  )]
                  ),
                 ( file_selector, segment_lesion_fu1,
                  [( 'fu1_t2', 'flair' )]
                  ),
                (file_selector, n4_baseline,
                  [( 'baseline_t1', 'input_image')]
                  ),
                ( bet_baseline, n4_baseline,
                [( 'mask_file', 'mask_image' )]
                ),
                  (file_selector, n4_fu1,
                   [( 'fu1_t1' , 'input_image' )]
                   ),
                  ( bet_fu1, n4_fu1,
                  [( 'mask_file', 'mask_image')]
                  ),
                 (file_selector, regt2t1_baseline,
                   [('baseline_t2','in_file')]
                    ),
                 (n4_baseline, regt2t1_baseline,
                  [('output_image', 'reference')]
                  ),
                  (file_selector, regt2t1_fu1,
                  [('fu1_t2', 'in_file')]
                  ),
                  (n4_fu1, regt2t1_fu1,
                   [('output_image', 'reference')]
                   ),
                  (regt2t1_baseline, regt2maskt1_baseline,
                  [('out_matrix_file', 'in_matrix_file')]
                  ),
                  (n4_baseline, regt2maskt1_baseline,
                  [('output_image', 'reference')]
                  ),
                  (segment_lesion_baseline, regt2maskt1_baseline,
                   [( 'flair_lesion', 'in_file' )]
                   ),
                  (regt2t1_fu1, regt2maskt1_fu1,
                  [('out_matrix_file', 'in_matrix_file')]
                  ),
                  (segment_lesion_fu1, regt2maskt1_fu1,
                  [('flair_lesion', 'in_file')]
                  ),
                  (n4_fu1, regt2maskt1_fu1,
                  [('output_image', 'reference')]
                  ),
                  (regt2maskt1_baseline, binarise_baseline,
                  [( 'out_file', 'in_file' )]
                  ),
                  ( regt2maskt1_fu1, binarise_fu1,
                  [( 'out_file', 'in_file')]
                  ),
                  (binarise_baseline,lesion_filler_baseline,
                  [('out_file', 'lesion_mask')]
                   ),
                  ( n4_baseline, lesion_filler_baseline,
                  [('output_image', 'in_file')]
                  ),
                  (binarise_fu1, lesion_filler_fu1,
                  [('out_file', 'lesion_mask')]
                  ),
                  (n4_fu1, lesion_filler_fu1,
                  [('output_image', 'in_file')]
                  )
                  ,
                  (lesion_filler_baseline, lister_node,
                  [( 'out_file', 'volume_baseline' )]
                  ),
                  ( lesion_filler_fu1, lister_node,
                  [( 'out_file', 'volume_fu1')]
                  ),
                  ( lister_node, robust_template_maker,
                  [('volume_list', 'moving_volumes')]
                  ),
                  ( robust_template_maker, robust_output_baseline_node,
                  [( 'moved_images', 'volume_list' )]
                  ),
                  ( robust_template_maker, robust_output_fu1_node,
                  [( 'moved_images', 'volume_list' )]
                  ),
                  (robust_output_baseline_node, gif_baseline,
                  [( 'volume_baseline', 't1')]
                  ),
                  (robust_output_fu1_node, gif_fu1,
                  [( 'volume_fu1', 't1' )]
                  ),
                  (robust_output_baseline_node, brain_steps_baseline,
                  [('volume_baseline', 't1' )]
                  ),
                  (robust_output_fu1_node, brain_steps_fu1,
                  [( 'volume_fu1', 't1' )]
                  )
                  ])

workflow.run()
