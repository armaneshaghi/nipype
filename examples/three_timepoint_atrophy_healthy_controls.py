##placeholders are as follows:
##{subject_id_to_replace}
##{baseline_t1_nii_gz}
##{fu1_t1_nii_gz}
##{fu2_t1_nii_gz}

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


subject_list = ['{subject_id_to_replace}']
workflow = pe.Workflow(name = 'second_wave')
workflow.base_dir = '/cluster/project0/MS_LATA/fourd/working/nipype'
infosource = pe.Node(interface = util.IdentityInterface(fields=['subject_id']), 
                                                          name = "infosource")
infosource.iterables = ('subject_id', subject_list)

templates = {{
            "baseline_t1" : '/cluster/project0/MS_LATA/fourd/patients/{{subject_id}}/{baseline_t1_nii_gz}',
            "fu1_t1" :  '/cluster/project0/MS_LATA/fourd/patients/{{subject_id}}/{fu1_t1_nii_gz}' ,
            "fu2_t1" :  '/cluster/project0/MS_LATA/fourd/patients/{{subject_id}}/{fu2_t1_nii_gz}' ,
                         }}

file_selector = pe.Node( SelectFiles(templates), "selectfiles") 

bet_baseline = pe.Node(name = 'bet_baseline',
                       interface = BET())
bet_baseline.inputs.mask = True

bet_fu1 = pe.Node(name = 'bet_fu1', 
                     interface = BET() )
bet_fu1.inputs.mask = True

bet_fu2 = pe.Node(name = 'bet_fu2', 
                     interface = BET() )
bet_fu2.inputs.mask = True

n4_baseline = pe.Node(name = 'n4_baseline', interface = N4BiasFieldCorrection())
n4_baseline.inputs.dimension = 3

n4_fu1 = pe.Node(name = 'n4_fu1', interface = N4BiasFieldCorrection() )
n4_fu1.inputs.dimension = 3

n4_fu2 = pe.Node(name = 'n4_fu2', interface = N4BiasFieldCorrection() )
n4_fu2.inputs.dimension = 3

def lister(volume_baseline, volume_fu1, volume_fu2):
    return [volume_baseline, volume_fu1,volume_fu2 ]

lister_node = pe.Node(name = 'lister_node' , 
                     interface = Function(input_names = ['volume_baseline', 
                                                        'volume_fu1',
                                                         'volume_fu2'],
                                         output_names = ['volume_list'],
                                      function = lister))

robust_template_maker = pe.Node(interface = mri_robust_template(),
                               name = 'mri_robust_template_maker'
                               )
robust_template_maker.inputs.template = 'within_sub.nii.gz'
robust_template_maker.inputs.moved_images = ['moved2template_baseline.nii.gz',
                                            'moved2template_fu1.nii.gz',
                                            'moved2template_fu2.nii.gz'
                                            ]
def return_baseline(volume_list):
    return volume_list[0]

def return_fu1(volume_list):
    return volume_list[1]

def return_fu2(volume_list):
    return volume_list[2]

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
robust_output_fu2_node = pe.Node(name = 'robust_output_fu2',
                     interface = Function(input_names = ['volume_list'],
                                          output_names = ['volume_fu2'],
                                          function = return_fu2
                                         ))

gif_baseline = pe.Node(interface = gif(),
                      name = 'gif_baseline')
gif_baseline.inputs.output_dir = 'gif_output'

gif_fu1 = pe.Node(interface = gif(),
                     name = 'gif_fu1')
gif_fu1.inputs.output_dir = 'gif_output'

gif_fu2 = pe.Node(interface = gif(),
                     name = 'gif_fu2')
gif_fu2.inputs.output_dir = 'gif_output'

brain_steps_baseline = pe.Node(interface = steps(),
                     name = 'brain_steps_baseline')
brain_steps_baseline.inputs.steps_mask = 'brain_steps_baseline_mask.nii.gz'

brain_steps_fu1 = pe.Node(interface =  steps(),
                              name = 'brain_steps_fu1')
brain_steps_fu1.inputs.steps_mask = 'brain_steps_fu1_mask.nii.gz'

brain_steps_fu2 = pe.Node(interface =  steps(),
                              name = 'brain_steps_fu2')
brain_steps_fu2.inputs.steps_mask = 'brain_steps_fu2_mask.nii.gz'


#check segmentation and CT estimation with 
baseline_ct_qa = pe.Node(interface = ct_qa_unified(),
                name = 'baseline_ct_qa')
baseline_ct_qa.inputs.output_dir = 'output_dir'

fu1_ct_qa = pe.Node(interface = ct_qa_unified(),
                name = 'fu1_ct_qa')
fu1_ct_qa.inputs.output_dir = 'output_dir'

fu2_ct_qa = pe.Node(interface = ct_qa_unified(),
                name = 'fu2_ct_qa')
fu2_ct_qa.inputs.output_dir = 'output_dir'

#calculate volumes
baseline_cal_vol = pe.Node(interface = calculateCTVol(),
                name = 'baseline_cal_vol')
baseline_cal_vol.inputs.summary_csv_file = 'summary.csv'

fu1_cal_vol = pe.Node(interface = calculateCTVol(),
                name = 'fu1_cal_vol')
fu1_cal_vol.inputs.summary_csv_file = 'summary.csv'

fu2_cal_vol = pe.Node(interface = calculateCTVol(),
                name = 'fu2_cal_vol')
fu2_cal_vol.inputs.summary_csv_file = 'summary.csv'

#data sink to conserve within-subject template otherwise it is deleted
datasink = pe.Node(nio.DataSink(), name='sinker')
datasink.inputs.base_directory = '/cluster/project0/MS_LATA/fourd/working/nipype/second_wave/'
workflow.connect(infosource, 'subject_id', datasink, 'container')
workflow.connect(robust_template_maker, 'template', datasink, 'within_subject_template')

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
                (file_selector, bet_fu2,
                 [( 'fu2_t1', 'in_file' )]
                 ),
                ( file_selector, n4_baseline,
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
                  (file_selector, n4_fu2,
                   [( 'fu2_t1' , 'input_image' )]
                   ),
                  ( bet_fu2, n4_fu2,
                  [( 'mask_file', 'mask_image')]
                  ),
                  ( n4_baseline, lister_node,
                  [( 'output_image', 'volume_baseline' )]
                  ),
                  ( n4_fu1, lister_node,
                  [( 'output_image', 'volume_fu1')]
                  ),
                   (n4_fu2, lister_node,
                  [( 'output_image', 'volume_fu2')]
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
                    ( robust_template_maker, robust_output_fu2_node,
                   [( 'moved_images', 'volume_list' )]
                  ),
                 ( robust_output_baseline_node, gif_baseline,
                  [( 'volume_baseline', 't1')]
                  ),
                  (robust_output_fu1_node, gif_fu1,
                  [( 'volume_fu1', 't1' )]
                  ),
                  (robust_output_fu2_node, gif_fu2,
                  [( 'volume_fu2', 't1' )]
                  ),
                    ( robust_output_baseline_node, brain_steps_baseline,
                   [('volume_baseline', 't1' )]
                  ),
                  (robust_output_fu1_node, brain_steps_fu1,
                  [( 'volume_fu1', 't1' )]
                  ),
                  (robust_output_fu2_node, brain_steps_fu2,
                  [( 'volume_fu2', 't1' )]
                  ),
                  (gif_baseline, baseline_ct_qa,
                  [( 'parcellation_file', 'gif_parcellation' )]
                  ),
                  (gif_fu1, fu1_ct_qa,
                  [('parcellation_file', 'gif_parcellation')]
                  ),
                  (gif_fu2, fu2_ct_qa,
                  [('parcellation_file', 'gif_parcellation')]
                  ),
                  (gif_baseline, baseline_ct_qa,
                  [('segmentation_file', 'gif_segmentation' )]
                  ),
                  (gif_fu1, fu1_ct_qa,
                  [('segmentation_file', 'gif_segmentation' )]
                  ),
                  (gif_fu2, fu2_ct_qa,
                  [('segmentation_file', 'gif_segmentation' )]
                  ),
                  (brain_steps_baseline, baseline_ct_qa,
                  [('steps_mask' , 'steps_mask' )]
                  ),
                  (brain_steps_fu1, fu1_ct_qa,
                  [('steps_mask' , 'steps_mask' )]
                  ),
                  (brain_steps_fu2, fu2_ct_qa,
                  [('steps_mask' , 'steps_mask' )]
                  ),
                  (robust_output_baseline_node, baseline_ct_qa,
                  [('volume_baseline', 't1_gif_space' )]
                  ),
                  (robust_output_fu1_node, fu1_ct_qa,
                  [('volume_fu1', 't1_gif_space' )]
                  ),
                  (robust_output_fu2_node, fu2_ct_qa,
                  [('volume_fu2', 't1_gif_space' )]
                  ),
                  (baseline_ct_qa, baseline_cal_vol,
                  [('gif_parcellation_steps_masked', 'parcellation_steps_multiplied')]
                  ),
                  (fu1_ct_qa, fu1_cal_vol,
                  [('gif_parcellation_steps_masked', 'parcellation_steps_multiplied')]
                  ),
                  (fu2_ct_qa, fu2_cal_vol,
                  [('gif_parcellation_steps_masked', 'parcellation_steps_multiplied')]
                  ),
                  (gif_baseline, baseline_cal_vol,
                  [('segmentation_file', 'gif_segmentation')]
                  ),
                  (gif_fu1, fu1_cal_vol,
                  [('segmentation_file', 'gif_segmentation')]
                  ),
                  (gif_fu2, fu2_cal_vol,
                  [('segmentation_file', 'gif_segmentation')]
                  ),
                  (baseline_ct_qa, baseline_cal_vol,
                  [('cortical_thickness_file', 'cortical_thickness_file')]
                  ),
                  (fu1_ct_qa, fu1_cal_vol,
                  [('cortical_thickness_file', 'cortical_thickness_file')]
                  ),
                  (fu2_ct_qa, fu2_cal_vol,
                  [('cortical_thickness_file', 'cortical_thickness_file')]
                  ),
                  (gif_baseline, baseline_cal_vol,
                  [('tiv_file', 'TIV_file')]
                  ),
                  (gif_fu1, fu1_cal_vol,
                  [('tiv_file', 'TIV_file')]
                  ),
                  (gif_fu2, fu2_cal_vol,
                  [('tiv_file', 'TIV_file')]
                  ),
                  (baseline_cal_vol, datasink,
                  [('summary_csv_file', 'baseline')]
                  ),
                  (fu1_cal_vol, datasink,
                  [('summary_csv_file', 'fu1' )]
                  ),
                  (fu2_cal_vol, datasink,
                  [('summary_csv_file', 'fu2' )]
                  )
                  ])

workflow.run()
