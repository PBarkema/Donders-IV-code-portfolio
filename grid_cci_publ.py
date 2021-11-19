# -*- coding: utf-8 -*-
"""
Created on Wed May 12 14:13:45 2021

@author: Pieter Barkema

This file aims to compute cci-values based on MEG-responses to objects of
different categories. It takes input from a .bash file to allow distributed
computation over different subjects and sessions simultaneously.
"""

if __name__ == '__main__':
    print("beginning...")
    import sys
    import pickle
    from cci_functions_publ import *
    
    # If script is called from shell check for parameters:
    if len(sys.argv) > 1:
        # Arrange all the input arguments
        subjects = [int(sys.argv[1])] # submitted as first, last, e.g. 1,15
#        if len(subject_arg) > 1:
#            subjects = range(int(subject_arg[0]),int(subject_arg[1])+1)
#        else:
#            subjects = [int(subject_arg[0])]
        print('Input arguments for processing:')

        sessions = [int(sys.argv[2])] # submitted as 1,2
#        if len(sessions_arg) > 1:
#            sessions = [int(sessions_arg[0]),int(sessions_arg[1])]
#        else:
#            sessions = [int(sessions_arg[0])]
        #print('Sessions: ')
        #print(sessions)
        hemi = str(sys.argv[4])
        labelset = sys.argv[5]
        print(labelset)
        labels = "".join(labelset.split(","))
        print(labels)
        
        # Convert left and right hemi to both
        if len(hemi)>1:
            hemi = "both"
    
    # source_estimate path
    data_dir = "/net/store/nbp/projects/informative-variance/source_estimates/"
    # if function is called directly (i.e. not from shell)
    #    subjects = [1]
    #    sessions = [1]
    results = {}
    # load the correct cortical areas for the current subject, and compute cci.
    for sub in subjects:
        for sess in sessions:
            sub = 'Cichy_s'+  str(sub)
            sess = '_sess'+str(sess)
            #TE1pTE2pFFCVVCVMV2VMV3PHA1PHA2PHA3
            fname_stc = data_dir + sub + sess + "/source_estimates_cond_" + str(hemi) + "_"+ "TE1pTE2pFFCVVCVMV2VMV3PHA1PHA2PHA3"
            open_file = open(fname_stc, "rb")
            loaded_list = pickle.load(open_file)
            open_file.close()
            # Load in the list of trials with the associated conditions
            fname_cond = data_dir + "/%s%s_conds" %(sub,sess)
            #save_to + "_" + "_".join(labellist) + "_conds"
            open_file = open(fname_cond, "rb")
            cond_list = pickle.load(open_file)
            open_file.close()

            cci = contrasted_class_information(loaded_list, cond_list)
            results[str(sub) + "_" + str(sess)] = cci
    # Save results.
    open_file = open("results_debug_" + "_" + sub + sess +"_"+ "cci" + "_sub_" + labelset, "wb")
    pickle.dump(results, open_file)
    print ('DONE')