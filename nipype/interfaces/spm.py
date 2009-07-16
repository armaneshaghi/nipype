"""
The spm module provides basic functions for interfacing with matlab and spm to 
access spm tools.

these functions include 
    
    Realign: within-modality registration

    SliceTiming : correcting differences in image acquisition time between slices

    Coregister: between modality registration
    
    Normalize: non-linear warping to standard space

    Segment: bias correction, segmentation


Need to get rid of pynifti dependency, build in brifti?
Get rid of nipy dependency, call this something else?




"""
from __future__ import with_statement

from nipype.interfaces.base import Bunch, CommandLine, setattr_on_read
from nifti import load
from nipype.interfaces.matlab import run_matlab_script, fltcols
from scipy.io import savemat
import numpy as np
import os



class SpmInfo(object):
    @setattr_on_read
    def spm_path(self):
        # fix with specified path
        with InTemporaryDirectory() as tmpdir:
            run_matlab_script("""
spm_path = spm('dir');
fid = fopen('spm_path.txt', 'wt');
fprintf(fid, '%s', spm_path);
fclose(fid);
""")
            spm_path = file('spm_path.txt', 'rt').read()
        return spm_path

spm_info = SpmInfo()


def make_job(jobtype, jobname, contents):
    return {'jobs':[{jobtype:[{jobname:contents}]}]}

def make_mfile(jobtype, jobname, contents):
    """ generates a mfile to build job structure"""
    
    mfile = '% generated by nipy.interfaces.spm\n'
    mfile += "spm_defaults;\n\n"

    subfield = contents[0].keys()[0]
    #mfile += "jobs{1}.%s{1}.%s.data.scans = {...\n"%(jobtype,jobname)
    #for item in contents[0][subfield]['data']:
    #    mfile += '%s;...\n'%(item[0])
    #mfile += '};\n'

    for key, value in contents[0][subfield].items():
        
        if type(value) == type(np.empty(1)):
            mfile += "jobs{1}.%s{1}.%s{1}.%s.%s = {...\n"%(jobtype,
                                                           jobname,
                                                           subfield,
                                                           key)
            for item in contents[0][subfield][key]:
                 mfile += '\'%s\';...\n'%(item[0])
            mfile += '};\n'
                
        if type(value) == type({}):
            for skey,val in contents[0][subfield][key].items():
                mfile += 'jobs{1}.%s{1}.%s{1}.%s.%s.%s = %s;\n'%(jobtype,
                                                                 jobname,
                                                                 subfield,
                                                                 key,
                                                                 skey,
                                                                 val)
    #print mfile
    mfile += 'spm_jobman(\'run\',jobs);'
    return mfile
    

def run_jobdef(jobdef):
    # fix with specified path
    with InTemporaryDirectory():
        savemat('pyjobs.mat', jobdef)
        matlab_out=run_matlab_script("""
load pyjobs;
spm_jobman('run', jobs);
""")
        return matlab_out

def scans_for_fname(fname):
    img = load(fname)
    n_scans = img.get_shape()[3]
    scans = np.zeros((n_scans, 1), dtype=object)
    for sno in range(n_scans):
        scans[sno] = '%s,%d' % (fname, sno+1)
    return scans


def scans_for_fnames(fnames):
    n_sess = len(fnames)
    sess_scans = np.zeros((1,n_sess), dtype=object)
    for sess in range(n_sess):
        sess_scans[0,sess] = scans_for_fname(fnames[sess])
    return sess_scans


def fname_presuffix(fname, prefix='', suffix='', use_ext=True):
    pth, fname = os.path.split(fname)
    fname, ext = os.path.splitext(fname)
    if not use_ext:
        ext = ''
    return os.path.join(pth, prefix+fname+suffix+ext)


def fnames_presuffix(fnames, prefix='', suffix=''):
    f2 = []
    for fname in fnames:
        f2.append(fname_presuffix(fname, prefix, suffix))
    return f2


class Realign(CommandLine):

    _cmd = None
    @property
    def cmd(self):
        """sets base command, not editable"""
        if self._cmd is None:
            self._cmd = 'spm_realign'
        return self._cmd

    def __init__(self, **opts):
        """use spm_realign for estimating within modality
           rigid body alignment

        Options
        -------

        To see optional arguments
        Realign().opts_help()


        Examples
        --------
        
        """

        super(Realign,self).__init__()
        self.args = []
        self._populate_opts()
        self.opts.update(**opts)
        self.cmdline = ''
        self.infile = ''
        self.outfile = ''
        
    def opts_help(self):
        doc = """
            Optional Parameters
            -------------------
            (all default to None and are unset)

            infile : list
                list of filenames to realign
            quality : float
                0.1 = fastest, 1.0 = most precise
                (spm5 default = 0.9)
            fwhm : float
                full width half maximum gaussian kernel 
                used to smoth images before realigning
                (spm default = 5.0)
            separation : float
                separation in mm used to sample images
                (spm default = 4.0)
            register_to_mean: Bool
                rtm if True uses a two pass method
                realign -> calc mean -> realign all to mean
                (spm default = False)
            weight_img : file
                filename of weighting image
                if empty, no weighting 
                (spm default = None)
            interp: float
                degree of b-spline used for interpolation
                (spm default = 2.0)
            wrap : list
                Check if interpolation should wrap in [x,y,z]
                (spm default = [0.0,0.0,0.0])
            
            """
        print doc

    def _populate_opts(self):
        self.opts = Bunch(infile=None,
                          quality=None,
                          fwhm=None,
                          separation=None,
                          register_to_mean=None,
                          weight_img=None,
                          interp=None,
                          wrap=None)
        
    def _validate(self):
        """validate spm realign options
        if set to None ignore
        """
        out_opts = []
        opts = {}
        eopts = {'eoptions':{}}
        [opts.update({k:v}) for k, v in self.opts.iteritems() if v is not None ]
        for opt in opts:
            if opt is 'infile':
                continue
            if opt is 'quality':
                eopts['eoptions'].update({'quality': float(opts[opt])})
                continue
            if opt is 'fwhm':
                eopts['eoptions'].update({'fwhm': float(opts[opt])})
                continue
            if opt is 'separation':
                eopts['eoptions'].update({'sep': float(opts[opt])})
                continue
            if opt is 'register_to_mean':
                eopts['eoptions'].update({'rtm': 1})
                continue
            if opt is 'weight_img':
                eopts['eoptions'].update({'weight': opts[opt]})
                continue
            if opt is 'interp':
                eopts['eoptions'].update({'interp': float(opts[opt])})
                continue
            if opt is 'wrap':
                if not len(opts[opt]) == 3:
                    raise ValueError('wrap must have 3 elements')
                eopts['eoptions'].update({'wrap': opts[opt]})
                continue
            print 'option %s not supported'%(opt)
        return eopts

    def run(self, infile=None, mfile=True):
        if infile is None:
            if self.opts.infile is None:
                raise ValueError('infile is not specified')
            else:
                infile = self.opts.infile
                
        newcoreg = self.update(infile=infile)
        job = newcoreg._compile_command(mfile)

        if mfile:
            out, cmdline = run_matlab_script(job, script_name='pyscript_spmrealign')
        else:
            out = run_jobdef(job)
            cmdline = ''

        newcoreg.out = out.output['out']
        newcoreg.retcode = out.output['returncode']
        newcoreg.err = out.output['err']
        newcoreg.cmdline = cmdline
        return newcoreg
        
        
    def _compile_command(self,mfile=True):
        """validates spm options and generates job structure
        if mfile is True uses matlab .m file
        else generates a job structure and saves in .mat
        """

        valid_opts = self._validate()
        if type(self.opts.infile) == type([]):
            sess_scans = scans_for_fnames(self.opts.infile)
        else:
            sess_scans = scans_for_fname(self.opts.infile)

        if mfile:
            # create an mfile
            if valid_opts is None:
                mfile = make_mfile('spatial','realign',[{
                                'estwrite':{
                                    'data':sess_scans,
                                    'eoptions':{}
                                    }
                                }]
                                    )
                
            else:
                key = valid_opts.keys()[0]
                vals = valid_opts[key]
                tmp = [{'estwrite':{'data':sess_scans,
                                    key: vals
                                    }}]
                mfile = make_mfile('spatial','realign',tmp)
                                    
                
            return mfile
        else:
            # create job structure .mat
            
            if valid_opts is None:
                
                job = make_job(('spatial', 'realign', [{
                                'estwrite':{
                                    'data':sess_scans,
                                    'eoptions': {}
                                    }
                                }]
                                ))
            else:
                key = valid_opts.keys()[0]
                vals = valid_opts[key]
                job = make_job(('spatial', 'realign', [{
                                'estwrite':{
                                    'data':sess_scans,
                                    key: vals
                                    }
                                }]
                                ))
                
                    
            return job
        
    def update(self, **opts):
        newrealign = Realign()
        [newrealign.opts.__setattr__(k,v) for k, v in self.opts.iteritems() if v is not None ]
        newrealign.opts.update(**opts)
        return newrealign
        
