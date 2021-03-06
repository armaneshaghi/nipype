import os
import glob
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
                    argstr = '%s',
                    mandatory = False)

class steps(NMRCommand):
      _cmd = ( '{home}/scripts/brain_steps_comic.sh'.format(home = home) )
      input_spec = stepsInputSpec
      output_spec = stepsOutputSpec
      def _format_arg(self, name, spec, value):
          if name == 'steps_mask':
              steps_mask =  self.inputs.steps_mask
              return '-output ' + os.path.abspath( steps_mask  )
          return super(steps, self)._format_arg(name, spec, value)
      def _list_outputs(self):
          outputs = self.output_spec().get()
          outputs['steps_mask'] = os.path.abspath(self.inputs.steps_mask)
          return outputs
      
#/home/aeshaghi/scripts/seg_GIF_comic.sh ${input} ${output_dir}
class gifInputSpec( NMRCommandInputSpec ):
      t1 = File(exists = True, position = 0, 
                      argstr = '%s', mandatory = True)
      output_dir = traits.String(argstr = '%s', position = 1, 
                      mandatory = False)

class gifOutputSpec( TraitedSpec ):
      segmentation_file = File(exists = True,
                      desc = 'multi-volume segmentation file from niftyReg or Gif')
      tiv_file = File(exists = True, desc = 'total intracranial volume image')
      parcellation_file =  File(exists = True, desc = 'gif parcellation file')
      Cerebellum_file = File(exists = True, desc = 'cerebellar file from gif')
      Brain_file = File(exists = True, desc = 'brain file')
      priors = File(exists = True, desc = 'priors file')
      bias_corrected = File(exists = True, desc = 't1 bias corrected image')

class gif(NMRCommand):
     _cmd = '{home}/scripts/seg_GIF_comic.sh'.format(
                     home = home)
     input_spec = gifInputSpec
     output_spec = gifOutputSpec
     
     def _format_arg(self, name, spec, value):
        if name == 'output_dir':
            output_dir =  os.getcwd()
            self.inputs.output_dir = output_dir
            print(output_dir)
            return output_dir
        return super(gif, self)._format_arg(name, spec, value)

     def _list_outputs(self):
        outputs = self.output_spec().get()
        output_dir = self.inputs.output_dir
        niftis = glob.glob(os.path.join(self.inputs.output_dir, "*.nii.gz"))
        outputs['segmentation_file'] = [f for f in niftis if 'Segmentation.nii.gz' in f][0]
        outputs['tiv_file'] = [ f for f in niftis if 'TIV.nii.gz' in f][0]
        outputs['parcellation_file'] = [f for f in niftis if 'Parcellation.nii.gz' in f ][0]
        outputs['Cerebellum_file'] = [ f for f in niftis if 'Cerebellum.nii.gz' in f ][0]
        outputs[ 'priors' ] = [f for f in niftis if 'NeuroMorph_prior.nii.gz' in f][0]
        outputs[ 'bias_corrected' ] = [f for f in niftis if 'NeuroMorph_BiasCorrected.nii.gz' in f][0] 
        outputs['Brain_file'] = [f for f in niftis if 'NeuroMorph_Brain.nii.gz' in f][0]
        return outputs
#/home/aeshaghi/scripts/segment_lesion.sh /cluster/project0/MS_LATA/fourd/patients/ROME_045/baseline_flair.nii.gz /cluster/project0/MS_LATA/fourd/patients/ROME_045/baseline_flair_lesion.nii.gz
class segmentLesionInputSpec( NMRCommandInputSpec ):
     flair = File(exists = True, position = 0, desc = 'flair',
                          argstr = "%s", mandatory = True)
     flair_lesion = File(argstr = "%s", position = 1, genfile = True,
                          hash_files = False,
                          desc = "flair segmented lesion")
class segmentLesionOutputSpec( TraitedSpec ):
     flair_lesion = File(exists = True, 
                          desc = 'generated lesion mask')
class segmentLesion( NMRCommand ):
     """
     flair lesion segmentaion, only set input flair and leave flair lesion to
     the program to define
     """

     _cmd = "/home/aeshaghi/scripts/segment_lesion.sh"
     input_spec = segmentLesionInputSpec
     output_spec = segmentLesionOutputSpec
     def _format_arg(self, name, spec, value):
        if name == 'flair':
            flair = self.inputs.flair
            return os.path.abspath( flair )
        elif name == 'flair_lesion':
            flair_lesion = os.path.abspath('flair_lesion.nii.gz')
            return flair_lesion
        return super(segmentLesion, self)._format_arg(name, spec, value)

     def _list_outputs(self):
        outputs = self.output_spec().get()
        outputs['flair_lesion'] = os.path.abspath('flair_lesion.nii.gz')
        return outputs
#/home/aeshaghi/scripts/ct_qa_unified.sh <t1_gif_space> <gif_segmentation> <gif_parcellation> <steps_mask> <output_dir>
class ct_qa_unifiedInputSpec( NMRCommandInputSpec ):
        t1_gif_space = File(exists = True, argstr = '%s', position = 0, 
                        desc = 'bias corrected T1 image, in the same space as GIF parcellation')
        gif_segmentation = File(exists = True, argstr = '%s',position = 1,
                desc = 'gif segmentation, which is multi-volume')
        gif_parcellation = File(exists = True, argstr = '%s',position = 2,
                desc = 'gif parcellation')
        steps_mask = File(exists = True, argstr = '%s',position = 3,
                desc = 'steps mask')
        output_dir = traits.String(argstr = '%s', position = 4, 
                      mandatory = False)

class ct_qa_unifiedOutputSpec( TraitedSpec ):
        cortical_thickness_file = File(exists = True,
                desc = 'cortical thickness file from KellyKapowski')
        gif_parcellation_steps_masked = File(exists = True,
                desc = 
                'parcellation from gif, which has been multiplied by steps mask to remove extra tissues')
        animated_X = File(exists = True,
                        desc = 'gif animation of axial slices')
        animated_Y = File(exists = True,
                        desc = 'gif animation of sagittal slices')
        animated_Z = File(exists = True,
                        desc = 'gif animation of coronal slices')

class ct_qa_unified( NMRCommand ):
        _cmd = '/home/aeshaghi/scripts/ct_qa_unified.sh'
        input_spec = ct_qa_unifiedInputSpec
        output_spec = ct_qa_unifiedOutputSpec

        def _format_arg(self, name, spec, value):
            if name == 'output_dir': 
                output_dir = self.inputs.output_dir
                return  os.path.abspath( output_dir )
            return super(ct_qa_unified, self)._format_arg(name, spec, value)

        def _list_outputs(self):
            outputs = self.output_spec().get()
            output_dir = self.inputs.output_dir
            outputs['cortical_thickness_file'] = os.path.abspath(os.path.join(
                    output_dir, 'ct.nii.gz'))
            outputs['gif_parcellation_steps_masked'] = os.path.abspath(os.path.join(
                    output_dir, 'gif_parcellation_steps.nii.gz'))
            outputs['animated_X'] = os.path.abspath(os.path.join(
                    output_dir, 'animated_X.gif'))
            outputs['animated_Y'] = os.path.abspath(os.path.join(
                    output_dir, 'animated_Y.gif'))
            outputs['animated_Z'] = os.path.abspath(os.path.join(
                    output_dir, 'animated_Z.gif'))

            return outputs
#/home/aeshaghi/scripts/calculateCTVol.py -p /cluster/project0/MS_LATA/fourd/working/gif/AMSTERDAM_4001/baseline/resampled_baseline_NeuroMorph_Parcellation_steps.nii.gz -s /cluster/project0/MS_LATA/fourd/working/gif/AMSTERDAM_4001/baseline/resampled_baseline_NeuroMorph_Segmentation.nii.gz -c /cluster/project0/MS_LATA/fourd/working/gif/AMSTERDAM_4001/baseline/ct.nii.gz -t /cluster/project0/MS_LATA/fourd/working/gif/AMSTERDAM_4001/baseline/resampled_baseline_NeuroMorph_TIV.nii.gz -o /cluster/project0/MS_LATA/fourd/working/gif/AMSTERDAM_4001/baseline/summary.csv

class calculateCTVolInputSpec( NMRCommandInputSpec ):
    parcellation_steps_multiplied = File(exists = True, position = 0,
            argstr = '-p %s',
            mandatory = True, desc = 'gif pacellation that has been multiplied with steps mask')
    gif_segmentation = File(exists = True, position = 1,
            argstr = '-s %s',
            mandatory = True, desc = 'gif segmentation, which is multi-volume')
    cortical_thickness_file = File(exists = True, position = 2,
            argstr = '-c %s', mandatory = True,
            desc = 'cortical thickness map file from KellyKapowski')
    TIV_file = File(exists = True, position = 3,
            argstr = '-t %s', mandatory = True,
            desc = 'TIV file used for tiv calculation')
    summary_csv_file = traits.String(argstr = '-o %s',
            position = 4 )
class calculateCTVolOutputSpec( TraitedSpec ):
    summary_csv_file = File(exists = True,
            desc = 'summary csv file reporting volume and thickness of gif')
class calculateCTVol( NMRCommand ):
    _cmd = '/home/aeshaghi/scripts/calculateCTVol.py'
    input_spec = calculateCTVolInputSpec
    output_spec = calculateCTVolOutputSpec

    def _format_arg(self, name, spec, value):
        if name == 'summary_csv_file':
            summary_csv_file =  self.inputs.summary_csv_file
            return  '-o ' + os.path.abspath( 'summary.csv' )
        return super(calculateCTVol, self)._format_arg(name, spec, value)

    def _list_outputs(self):
        outputs = self.output_spec().get()
        summary_csv_file = self.inputs.summary_csv_file
        outputs['summary_csv_file'] = os.path.abspath( 'summary.csv'  )
        return outputs

    

