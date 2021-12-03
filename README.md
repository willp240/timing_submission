# Scintillator Timing Parameter Tuning
Scripts for submitting jobs for the scintillation timing tuning.

The main submission script is heavily based upon Josie's rat submission: https://gitlab.physics.ox.ac.uk/patonj/rat_submission
But is modified for the specific purpose of scanning through different values of the scintillation timing parameters.

The idea is you edit the variables at the top of submitJobs.py to be the values you want to scroll through.
Then running submitJobs.py goes through nested for loops to get each combination of parameter values.
For each combination:

- A macro is written based on the input macro you give it, with updated timing parameter values

- A condor .sh file is produced, based on condor_base.mac, with the appropriate rat macro and job name based on the updated timing parameters

- A job is submitted to condor, running simulation for the given rat macro and updated timing parameters
  

**Intended Usage**

>python submitJobs.py BiPo214_scint_beta.mac /path/to/output/directory/

with options:

  -e Path to environment file
  Default: /data/snoplus3/scint_time_team/rat/env.sh

  -s Path to submission directory
  Default: /data/snoplus3/scint_time_team/timing_submission

  -d Path to run directory (RAT)
  Default: /data/snoplus3/scint_time_team/rat/

  -n Run number
  Default: 270166

The defaults are set so that in theory we can just run with:

>python submitJobs.py BiPo214_scint_beta.mac /path/to/output/directory

(or similarly for alpha). I think having fewer required arguments on the commmand line should reduce the chance of human error.
The default run number will be different for each PPO concentration though. The default file paths are hard coded to specific
locations on the Oxford PPLX clusters. It has not been designed as a general tool that could be ready to run anywhere out the 
box at the moment. If you were to do the tuning elsewhere these would need to be changed, but hopefully this repository would
still be useful as a starting point.


**Parameter Scan**

In theory you could scan through N values for each parameter all in one go, but the number of jobs will quickly balloon.
So it's probably better to scan through several values for one parameter while others are fixed, and do this for each parameter
one-by-one. In which case the script would be run as above for several values of e.g t1, but only value of each of the others.
Goverened by the results of that, t1 would then be fixed in submitJobs.py, and t2 set to several values, and so on and so forth.

With having separate macros for alpha and beta, the idea is alpha and beta parameter scans can be run simultaneously. The only difference 
between the two variables is which RAT DB variables get updated with the new parameter values.

This is all then repeated for each PPO concentration required


**Notes**

For quick tests, you can run over a small amount of events per job by adding " -n 1" (or similar) to the end of the last line
in condor_base.mac
