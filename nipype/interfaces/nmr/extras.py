import os
import stat

def write_two_timepoint_pipeline(baseline_t1_file_name, 
                                 baseline_t2_file_name,
                                 baseline_t2_lesion_mask, fu1_t1_file_name, fu1_t2_file_name, 
                                 fu1_t2_lesion_mask, 
                                folder_name, script_full_path):
    '''
    NB: all nifti files must come with their extension (nii.gz)
    
    '''

    with open('/home/aeshaghi/nipype_development/nipype/examples/two_timepoint_atrophy.py', 
              'r') as textFile:
        pipeline_template = textFile.readlines()
    
    #consolidate everything into one string for placeholder replacement
    pipeline_template = " ".join(pipeline_template)
    filled_pipeline = pipeline_template.format( 
    baseline_t1_nii_gz = baseline_t1_file_name,
    baseline_t2_nii_gz = baseline_t2_file_name,
    baseline_t2_lesion_mask_nii_gz = baseline_t2_lesion_mask,
    fu1_t1_nii_gz = fu1_t1_file_name,
    fu1_t2_nii_gz = fu1_t2_file_name,
    fu1_t2_lesion_mask_nii_gz = fu1_t2_lesion_mask,
    subject_id_to_replace = folder_name
    )
    list_string = []
    for line in filled_pipeline.split('\n'):
        #for strange reasons, one space ends up at the beginning
        #of lines so we need to remove it
        new_line = line[1:]
        list_string.append(new_line)
        
    with open(script_full_path, 'w') as textFile:
        for line in list_string:
            textFile.write(line + '\n')
    return None


def write_two_timepoint_with_lesion_segmentation_pipeline(
               baseline_t1_file_name,
                baseline_t2_file_name,
                fu1_t1_file_name,
                fu1_t2_file_name, 
                script_full_path,
                folder_name):
    
    with open(
        '/home/aeshaghi/nipype_development/nipype/examples/two_timepoint_atrophy_with_lesion_segmentation.py', 
          'r') as textFile:
        pipeline_template = textFile.readlines()
    
    #consolidate everything into one string for placeholder replacement
    pipeline_template = " ".join(pipeline_template)
    filled_pipeline = pipeline_template.format( 
    baseline_t1_nii_gz = baseline_t1_file_name,
    baseline_t2_nii_gz = baseline_t2_file_name,
    fu1_t1_nii_gz = fu1_t1_file_name,
    fu1_t2_nii_gz = fu1_t2_file_name,
    subject_id_to_replace = folder_name
    )
    list_string = []
    for line in filled_pipeline.split('\n'):
        #for strange reasons, one space ends up at the beginning
        #of lines so we need to remove it
        new_line = line[1:]
        list_string.append(new_line)
        
    with open(script_full_path, 'w') as textFile:
        for line in list_string:
            textFile.write(line + '\n')
    return None


def write_two_timepoint_pipeline_hc(baseline_t1_file_name, 
                                      fu1_t1_file_name, 
                                       folder_name, 
                                       script_full_path):
    '''
    NB: all nifti files must come with their extension (nii.gz)
    
    '''

    with open('/home/aeshaghi/nipype_development/nipype/examples/two_timepoint_atrophy_healthy_controls.py', 
              'r') as textFile:
        pipeline_template = textFile.readlines()
    
    #consolidate everything into one string for placeholder replacement
    pipeline_template = " ".join(pipeline_template)
    filled_pipeline = pipeline_template.format( 
    baseline_t1_nii_gz = baseline_t1_file_name,
    fu1_t1_nii_gz = fu1_t1_file_name,
    subject_id_to_replace = folder_name
    )
    list_string = []
    for line in filled_pipeline.split('\n'):
        #for strange reasons, one space ends up at the beginning
        #of lines so we need to remove it
        new_line = line[1:]
        list_string.append(new_line)
        
    with open(script_full_path, 'w') as textFile:
        for line in list_string:
            textFile.write(line + '\n')
    return None

def write_three_timepoint_pipeline(baseline_t1_file_name, 
                                   baseline_t2_file_name,
                                   baseline_t2_lesion_mask, 
                                   fu1_t1_file_name,
                                   fu1_t2_file_name, 
                                   fu1_t2_lesion_mask, 
                                   fu2_t1_file_name,
                                   fu2_t2_file_name, 
                                   fu2_t2_lesion_mask,
                                   folder_name, 
                                   script_full_path):
    '''
    NB: all nifti files must come with their extension (nii.gz)
    
    '''

    with open('/home/aeshaghi/nipype_development/nipype/examples/three_timepoint_atrophy.py', 
              'r') as textFile:
        pipeline_template = textFile.readlines()
    
    #consolidate everything into one string for placeholder replacement
    pipeline_template = " ".join(pipeline_template)
    filled_pipeline = pipeline_template.format( 
    baseline_t1_nii_gz = baseline_t1_file_name,
    baseline_t2_nii_gz = baseline_t2_file_name,
    baseline_t2_lesion_mask_nii_gz = baseline_t2_lesion_mask,
    fu1_t1_nii_gz = fu1_t1_file_name,
    fu1_t2_nii_gz = fu1_t2_file_name,
    fu1_t2_lesion_mask_nii_gz = fu1_t2_lesion_mask,
    fu2_t1_nii_gz = fu2_t1_file_name,
    fu2_t2_nii_gz = fu2_t2_file_name,
    fu2_t2_lesion_mask_nii_gz = fu2_t2_lesion_mask,
    subject_id_to_replace = folder_name
    )
    list_string = []
    for line in filled_pipeline.split('\n'):
        #for strange reasons, one space ends up at the beginning
        #of lines so we need to remove it
        new_line = line[1:]
        list_string.append(new_line)
        
    with open(script_full_path, 'w') as textFile:
        for line in list_string:
            textFile.write(line + '\n')
    return None

def write_three_timepoint_with_lesion_segmentation_pipeline(
                baseline_t1_file_name,
                baseline_t2_file_name,
                fu1_t1_file_name,
                fu1_t2_file_name, 
                fu2_t1_file_name,
                fu2_t2_file_name, 
                script_full_path,
                folder_name):
    
    with open(
        '/home/aeshaghi/nipype_development/nipype/examples/three_timepoint_atrophy_with_lesion_segmentation.py', 
          'r') as textFile:
        pipeline_template = textFile.readlines()
    
    #consolidate everything into one string for placeholder replacement
    pipeline_template = " ".join(pipeline_template)
    filled_pipeline = pipeline_template.format( 
    baseline_t1_nii_gz = baseline_t1_file_name,
    baseline_t2_nii_gz = baseline_t2_file_name,
    fu1_t1_nii_gz = fu1_t1_file_name,
    fu1_t2_nii_gz = fu1_t2_file_name,
    fu2_t1_nii_gz = fu2_t1_file_name,
    fu2_t2_nii_gz = fu2_t2_file_name,
    subject_id_to_replace = folder_name
    )
    list_string = []
    for line in filled_pipeline.split('\n'):
        #for strange reasons, one space ends up at the beginning
        #of lines so we need to remove it
        new_line = line[1:]
        list_string.append(new_line)
        
    with open(script_full_path, 'w') as textFile:
        for line in list_string:
            textFile.write(line + '\n')
    return None

def write_three_timepoint_pipeline_hc(baseline_t1_file_name, 
                                       fu1_t1_file_name, 
                                       fu2_t1_file_name, 
                                       folder_name, 
                                       script_full_path):
    '''
    NB: all nifti files must come with their extension (nii.gz)
    
    '''

    with open('/home/aeshaghi/nipype_development/nipype/examples/three_timepoint_atrophy_healthy_controls.py', 
              'r') as textFile:
        pipeline_template = textFile.readlines()
    
    #consolidate everything into one string for placeholder replacement
    pipeline_template = " ".join(pipeline_template)
    filled_pipeline = pipeline_template.format( 
    baseline_t1_nii_gz = baseline_t1_file_name,
    fu1_t1_nii_gz = fu1_t1_file_name,
    fu2_t1_nii_gz = fu2_t1_file_name,
    subject_id_to_replace = folder_name
    )
    list_string = []
    for line in filled_pipeline.split('\n'):
        #for strange reasons, one space ends up at the beginning
        #of lines so we need to remove it
        new_line = line[1:]
        list_string.append(new_line)
        
    with open(script_full_path, 'w') as textFile:
        for line in list_string:
            textFile.write(line + '\n')
    return None

def write_four_timepoint_pipeline(baseline_t1_file_name, 
                                   baseline_t2_file_name,
                                   baseline_t2_lesion_mask, 
                                   fu1_t1_file_name,
                                   fu1_t2_file_name, 
                                   fu1_t2_lesion_mask, 
                                   fu2_t1_file_name,
                                   fu2_t2_file_name, 
                                   fu2_t2_lesion_mask,
                                   fu3_t1_file_name,
                                   fu3_t2_file_name, 
                                   fu3_t2_lesion_mask,
                                   folder_name, 
                                   script_full_path):
    '''
    NB: all nifti files must come with their extension (nii.gz)
    
    '''

    with open('/home/aeshaghi/nipype_development/nipype/examples/four_timepoint_atrophy.py', 
              'r') as textFile:
        pipeline_template = textFile.readlines()
    
    #consolidate everything into one string for placeholder replacement
    pipeline_template = " ".join(pipeline_template)
    filled_pipeline = pipeline_template.format( 
    baseline_t1_nii_gz = baseline_t1_file_name,
    baseline_t2_nii_gz = baseline_t2_file_name,
    baseline_t2_lesion_mask_nii_gz = baseline_t2_lesion_mask,
    fu1_t1_nii_gz = fu1_t1_file_name,
    fu1_t2_nii_gz = fu1_t2_file_name,
    fu1_t2_lesion_mask_nii_gz = fu1_t2_lesion_mask,
    fu2_t1_nii_gz = fu2_t1_file_name,
    fu2_t2_nii_gz = fu2_t2_file_name,
    fu2_t2_lesion_mask_nii_gz = fu2_t2_lesion_mask,
    fu3_t1_nii_gz = fu3_t1_file_name,
    fu3_t2_nii_gz = fu3_t2_file_name,
    fu3_t2_lesion_mask_nii_gz = fu3_t2_lesion_mask,
    subject_id_to_replace = folder_name
    )
    list_string = []
    for line in filled_pipeline.split('\n'):
        #for strange reasons, one space ends up at the beginning
        #of lines so we need to remove it
        new_line = line[1:]
        list_string.append(new_line)
        
    with open(script_full_path, 'w') as textFile:
        for line in list_string:
            textFile.write(line + '\n')
    return None

def write_four_timepoint_with_lesion_segmentation_pipeline(
                baseline_t1_file_name,
                baseline_t2_file_name,
                fu1_t1_file_name,
                fu1_t2_file_name, 
                fu2_t1_file_name,
                fu2_t2_file_name, 
                fu3_t1_file_name,
                fu3_t2_file_name, 
                script_full_path,
                folder_name):
    
    with open(
        '/home/aeshaghi/nipype_development/nipype/examples/four_timepoint_atrophy_with_lesion_segmentation.py', 
          'r') as textFile:
        pipeline_template = textFile.readlines()
    
    #consolidate everything into one string for placeholder replacement
    pipeline_template = " ".join(pipeline_template)
    filled_pipeline = pipeline_template.format( 
    baseline_t1_nii_gz = baseline_t1_file_name,
    baseline_t2_nii_gz = baseline_t2_file_name,
    fu1_t1_nii_gz = fu1_t1_file_name,
    fu1_t2_nii_gz = fu1_t2_file_name,
    fu2_t1_nii_gz = fu2_t1_file_name,
    fu2_t2_nii_gz = fu2_t2_file_name,
    fu3_t1_nii_gz = fu3_t1_file_name,
    fu3_t2_nii_gz = fu3_t2_file_name,
    subject_id_to_replace = folder_name
    )
    list_string = []
    for line in filled_pipeline.split('\n'):
        #for strange reasons, one space ends up at the beginning
        #of lines so we need to remove it
        new_line = line[1:]
        list_string.append(new_line)
        
    with open(script_full_path, 'w') as textFile:
        for line in list_string:
            textFile.write(line + '\n')
    return None

def write_four_timepoint_pipeline_hc(baseline_t1_file_name, 
                                       fu1_t1_file_name, 
                                       fu2_t1_file_name, 
                                       fu3_t1_file_name, 
                                       folder_name, 
                                       script_full_path):
    '''
    NB: all nifti files must come with their extension (nii.gz)
    
    '''

    with open('/home/aeshaghi/nipype_development/nipype/examples/four_timepoint_atrophy_healthy_controls.py', 
              'r') as textFile:
        pipeline_template = textFile.readlines()
    
    #consolidate everything into one string for placeholder replacement
    pipeline_template = " ".join(pipeline_template)
    filled_pipeline = pipeline_template.format( 
    baseline_t1_nii_gz = baseline_t1_file_name,
    fu1_t1_nii_gz = fu1_t1_file_name,
    fu2_t1_nii_gz = fu2_t1_file_name,
    fu3_t1_nii_gz = fu3_t1_file_name,
    subject_id_to_replace = folder_name
    )
    list_string = []
    for line in filled_pipeline.split('\n'):
        #for strange reasons, one space ends up at the beginning
        #of lines so we need to remove it
        new_line = line[1:]
        list_string.append(new_line)
        
    with open(script_full_path, 'w') as textFile:
        for line in list_string:
            textFile.write(line + '\n')
    return None

def write_bash_script(python_script_path, bash_script_path, longevity):
        '''
        Use me to write bash scripts for SGE in cs cluster
        python_script_path and bash_script_path are both
        longevity: the time requested, in hours (an integer), from cs cluster
        '''
        #sge directives, customise according to needs
        string = '''
#$ -S /bin/bash
#$ -cwd
#$ -l h_rt={longevity}:00:0
#$ -V
#$ -j y
#$ -R y
#$ -pe smp 4
#$ -l h_vmem=8G
#$ -l tmem=8G
#$ -l tscratch=30G
source activate development
python {python_script}'''.format(python_script = python_script_path,
                longevity = str(longevity))
        with open(bash_script_path, 'w') as textFile:
                textFile.write(string)
        st = os.stat( bash_script_path )
        os.chmod( bash_script_path , st.st_mode | stat.S_IEXEC)

        return None

def is_folder_created_after_specific_date( folder_full_path , specific_date):
         '''
         use this to test whether the folder has been created after the specific date
         inputs:
         =======

         specific date should be in the format similar to:
         
         '01-Apr-2016'
         '''

         import time
         folder_creation_date = time.ctime(os.path.getctime( folder_full_path ))
         cd_date_format = folder_creation_date.split()[2] + '-' + folder_creation_date.split()[1] + '-' + \
         folder_creation_date.split()[-1]
         cd_date_struct = time.strptime( cd_date_format, '%d-%b-%Y')
         reference_date = time.strptime( specific_date, '%d-%b-%Y')
         
         return cd_date_struct > reference_date
