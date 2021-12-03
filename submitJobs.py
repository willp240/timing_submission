import sys
import os
import string
import argparse
    
def write_macro(mac, macname, outfile, t1, t2, t3, A1, A2, A3, tR):
    with open(macname, "w") as f:
        f.write(mac.format(os.path.abspath(outfile), t1, t2, t3, A1, A2, A3, tR))

def check_dir(dname):
    """Check if directory exists, create it if it doesn't"""
    if(dname[-1] != "/"):
        dname = dname + "/"
    direc = os.path.dirname(dname)
    try:
        os.stat(direc)
    except:
        os.makedirs(direc)
        print "Made directory %s...." % dname
    return dname

def pycondor_submit(job_batch, job_id, macro_path, run_path, rat_env, sub_path, run_num, out_dir, sleep_time = 1, priority = 5):
    '''
    submit a job to condor, write a sh file to source environment and execute command
    then write a submit file to be run by condor_submit
    '''

    print job_id

    ### set a condor path to be called later
    
    condor_path = "{0}/".format(out_dir)

    ### write sh file (which sources environments, runs commands)

    base_filename = "{0}/condor_base.mac".format(sub_path)
    in_macro_file = open(base_filename, "r")
    raw_text = string.Template(in_macro_file.read())
    in_macro_file.close()

    other_commands = ''
    out_macro_text = raw_text.substitute(sh_sub=rat_env, mac_sub=macro_path, run_directory_sub=run_path, other_commands_sub=other_commands, run_number=run_num)

    sh_filepath = "{0}/sh/".format(condor_path)+str(job_id).replace("/", "")+'.sh'
    if not os.path.exists(os.path.dirname(sh_filepath)):
        os.makedirs(os.path.dirname(sh_filepath))
    sh_file = open(sh_filepath, "w")
    sh_file.write(out_macro_text)
    sh_file.close()
    os.chmod(sh_filepath, 0o777)
    
    ### now create submit file
    error_path = os.path.abspath('{0}/error'.format(condor_path))
    output_path = os.path.abspath('{0}/output'.format(condor_path))
    log_path = os.path.abspath('{0}/log'.format(condor_path))
    submit_path = os.path.abspath('{0}/submit'.format(condor_path))

    universe = "vanilla"
    notification = "never"
    n_rep = 1
    getenv = "False" # "False"

    submit_filepath = os.path.join(submit_path, job_id)
    submit_filepath += ".submit"
    out_submit_text = "executable              = "+str(sh_filepath)+"\n"+\
                     "universe                = "+str(universe)+"\n"+\
                     "output                  = "+str(output_path)+"/"+str(job_id)+".output\n"+\
                     "error                   = "+str(error_path)+"/"+str(job_id)+".error\n"+\
                     "log                     = "+str(log_path)+"/"+str(job_id)+".log\n"+\
                     "notification            = "+str(notification)+"\n"+\
                     "priority                = "+str(priority)+"\n"+\
                     "getenv                  = "+str(getenv)+"\n"+\
                     "queue "+str(n_rep)+"\n"

    ## check and create output path
    if not os.path.exists(os.path.dirname(submit_filepath)):
        os.makedirs(os.path.dirname(submit_filepath))
    out_submit_file = open(submit_filepath, "w")
    out_submit_file.write(out_submit_text)
    out_submit_file.close()
    
    command = 'condor_submit -batch-name \"'+job_batch+'\" '+submit_filepath
    print "executing job: "+command
    os.system(command)


if __name__ == "__main__":

    parser = argparse.ArgumentParser("Launch a load of identical rat simulation jobs")
    parser.add_argument('macro', type=str, help='template macro file to load')
    parser.add_argument('out_dir', type=str, help='directory to place reprocessed files')
    parser.add_argument('-e', '--env_file', type=str,
                        help='path to environment file',
                        default="/data/snoplus3/scint_time_team/rat/env.sh")
    parser.add_argument("-s", "--submission_directory", type=str,
                       default="/data/snoplus3/scint_time_team/timing_submission",
                       help="path to the directory this file is in, for outputs and inputs")
    parser.add_argument("-d", "--run_directory", type=str,
                       default="/data/snoplus3/scint_time_team/rat/",
                       help="base directory from which the scripts will be run")
    parser.add_argument("-n", "--run_number", type=str,
                        default="270166",
                        help="which run number do you want to run for?")
    args = parser.parse_args()

    ## check that macros is readable
    try:
        mac = open(args.macro, "r").read()
    except:
        print "template macro could not be read"
        sys.exit(1)

    ## check if output and condor directories exist, create if they don't
    out_dir = check_dir(args.out_dir)

    condor_directory = "{0}/condor".format(args.submission_directory)

#    condor_dir = check_dir(condor_directory)
    log_dir = check_dir("{0}/log/".format(out_dir))
    error_dir = check_dir("{0}/error/".format(out_dir))
    mac_dir = check_dir("{0}/macros/".format(out_dir))
    sh_dir = check_dir("{0}/sh/".format(out_dir))
    submit_dir = check_dir("{0}/submit/".format(out_dir))
    output_dir = check_dir("{0}/output/".format(out_dir))
    base_name = args.macro.split("/")[-1].replace(".mac","")

    t1values = 7.19, 
    t2values = 24.81,
    t3values = 269.87, 
    A1values = 0.553, 
    A2values = 0.331, 
    A3values = 0.116, 
    tRvalues = 0.9, 

    for t1 in t1values:
        for t2 in t2values:
            for t3 in t3values:
                for A1 in A1values:
                    for A2 in A2values:
                        for A3 in A3values:
                            for tR in tRvalues:

                                write_macro(mac,
                                            "{0}{1}_t1_{2}__t2_{3}__t3_{4}__A1_{5}__A2_{6}__A3_{7}__tR_{8}.mac".format(mac_dir, base_name, t1, t2, t3, A1, A2, A3, tR),
                                            "{0}{1}_t1_{2}__t2_{3}__t3_{4}__A1_{5}__A2_{6}__A3_{7}__tR_{8}".format(out_dir, base_name, t1, t2, t3, A1, A2, A3, tR),
                                            t1, t2, t3, A1, A2, A3, tR
                                )
        
                                job_id = "{0}_t1_{1}__t2_{2}__t3_{3}__A1_{4}__A2_{5}__A3_{6}__tR_{7}".format(base_name, t1, t2, t3, A1, A2, A3, tR)
                                batch_id = "timing_{0}".format(base_name)
                                pycondor_submit(batch_id,job_id,"{0}{1}_t1_{2}__t2_{3}__t3_{4}__A1_{5}__A2_{6}__A3_{7}__tR_{8}.mac".format(mac_dir,base_name, t1, t2, t3, A1, A2, A3, tR), args.run_directory, args.env_file, args.submission_directory, args.run_number, out_dir, sleep_time = 1, priority = 5)
