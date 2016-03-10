import os
from .base import NMRCommandInputSpec,NMRCommand, find_arman_home
from ..base import TraitedSpec, File, traits, InputMultiPath, OutputMultiPath, isdefined


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
      home = find_arman_home()
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

