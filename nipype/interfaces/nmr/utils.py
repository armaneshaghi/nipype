import os
from .base import NMRCommandInputSpec,NMRCommand, find_arman_home
from ..base import TraitedSpec, File, traits, InputMultiPath, OutputMultiPath, isdefined
home = find_arman_home()

class thicknessInputSpec(NMRCommandInputSpec):
      gif_segmentation = File(exists=True,
                        argstr='-s %s', mandatory=True)

class thicknessOutputSpec(TraitedSpec):
      cortical_thickness_image = File(exists=True)

class thickness(NMRCommand):
      """
      Registration based cortical thicknes analysis based on ANTs' DIRECT algorithm

      Examples
      --------
      
      >>> from nipype.interfaces.nmr.utils import thickness
      >>> ct = ct()
      >>> ct.inputs.gif_sementation = 'structural.nii'
      'python thicknessWrapper.py -s structural.nii'
      """
      _cmd = '{home}/anaconda/envs/development/bin/python {home}/scripts/thicknessWrapper.py'.format(
                      home = home)
      input_spec = thicknessInputSpec 
      output_spec = thicknessOutputSpec

      def _run_interface(self, runtime):
        segmentation_path = self.inputs.gif_segmentation
        runtime = super(thickness, self)._run_interface(runtime)
        return runtime

      def _list_outputs(self):
        outputs = self._outputs().get()
        gifDir = os.path.dirname(self.inputs.gif_segmentation )
        outputs['cortical_thickness_image'] = os.path.join(gifDir,'ct.nii.gz' )
        return outputs

class stepsInputSpec( NMRCommandInputSpec ):
      t1 = File(exists = True, position = 0,
                    argstr = '-input %s',
                    mandatory = True)
      steps_mask = File(argstr = '-output %s' )

class stepsOutputSpec(TraitedSpec):
      steps_mask = File(exists = True, position = 1,
                    argstr = '-output %s',
                    mandatory = False)

class steps(NMRCommand):
      _cmd = ( '{home}/scripts/brain_steps_comic.py'.format(home = home) )
      input_spec = stepsInputSpec
      output_spec = stepsOutputSpec
      
#/home/aeshaghi/scripts/seg_GIF_comic.sh ${input} ${output_dir}
class gifInputSpec( NMRCommandInputSpec ):
      t1 = File(exists = True, position = 0, 
                      argstr = '%s', mandatory = True)
      output_dir = traits.String(argstr = '%s', position = 1, 
                      mandatory = True)

class gifOutputSpec( TraitedSpec ):
      segmentation_file = File(exists = True,
                      desc = 'multi-volume segmentation file from niftyReg or Gif')
      tiv_file = File(exists = True, desc = 'total intracranial volume image')
      parcellation_file =  File(exists = True, desc = 'gif parcellation file')
      Cerebellum_file = File(exists = True, desc = 'cerebellar file from gif')
      Brain_file = File(exists = True, desc = 'brain file')
      priors = File(exists = True, desc = 'priors file')
      bias_corrected = File(exists = True, 't1 bias corrected image')

class gif(NMRCommand):
     _cmd = '{home}/scripts/seg_GIF_comic.sh'.format(
                     home = home)
     input_spec = thicknessInputSpec 
     output_spec = thicknessOutputSpec

      def _list_outputs(self):
          outputs = self.output_spec().get()
          t1 = self.inputs.t1
          t1_name = t1.split('.')[0]
          output_dir = self.inputs.output_dir
          outputs['segmentation_file'] = os.path.abspath(os.path.join(
                  output_dir, t1_name + '_t1_' + 'NeuroMorph_' +
                  'Segmentation.nii.gz')
          outputs['tiv_file'] = os.path.abspath(os.path.join(
                  output_dir, t1_name + '_t1_' + 'NeuroMorph_' + 
                  'TIV.nii.gz')
          outputs['parcellation_file'] = os.path.abspath(os.path.join(
                  output_dir, t1_name + '_t1_' + 'NeuroMorph_' +
                  'Parcellation.nii.gz'))
          outputs['Cerebellum_file'] = os.path.abspath(os.path.join(
                  output_dir, t1_name + '_t1_' + 'Cerebellum.nii.gz' ))
          outputs[ 'priors' ] = os.path.abspath(os.path.join(output_dir,
                  t1_name + '_t1_' + 'NeuroMorph_prior.nii.gz' ))
          outputs[ 'bias_corrected' ] = os.path.abspath(os.path.join(output_dir,
                  t1_name + '_t1_' + 'NeuroMorph_BiasCorrected.nii.gz' ))
          outputs['Brain_file'] = os.path.abspath(os.path.join(output_dir,
                  output_dir, t1_name + '_t1_' + 'NeuroMorph_Brain.nii.gz'))
          return outputs

