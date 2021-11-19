# -*- coding: utf-8 -*-
"""
Created on Mon Jul 19 14:57:06 2021

@author: Pieter Barkema

Contrasted class information (cci) seeks to compute how much variance is shared 
between trial-by-trial variability to an object and its class opposed to any other
object category. The function takes our previously estimated MEG source estimates 
and outputs an asymmetric matrix of shared information between object and 
class responses.

Functions:
contrasted_class_information: main function to compute cci per object category.
    class_alignment: preprocesses the data and computes parallelized.
        exemp_var: normalizes and structures MEG-response data.
        distr_cci_computation: parallelized function to process different MEG time steps.
            class_var: computes shared variance between object and class responses.
            
Input: a list of spatiotemporal MEG-data and trial numbers; 
       a list of stimulus numbers.
"""

def contrasted_class_information(source_list, trial_list):
    """
        This function loads the cci-algorithm with the appropriate object
        categories, and returns the right dictionary format of results.
        
        Parameters
        ----------
        source_list: spatiotemporal MEG-data with trial numbers in MNE format.
        trial_list: a list of trials coupled with the stimulus number.
    """
    import numpy as np
    
    # Hard-coded lower and upper bound of stimulus subcategorizations.    
    # human body parts, faces, animal parts, faces, natural objects, manmade objects
    low_cat_ind = [1,13,25,37,49,72,93]
    # human, animal, natural, manmade
    mid_cat_ind = [1,25,49,72]
    # animate, inanimate
    high_cat_ind = [1,49]
    
    cat_idx = low_cat_ind

    ccis = {}
    # Calculates the contrasted class information for every object class
    for in_class in cat_idx[:-1]:
        # Creates indices for every in-class and out-class.
        out_class_inds = []
        for obj_class in range(len(cat_idx)-1):
            if cat_idx[obj_class] == in_class:
                begin_idx_in = cat_idx[obj_class]
                end_idx_in = cat_idx[obj_class+1]
                in_class= [begin_idx_in, end_idx_in-1]
            else:
                begin_idx_out = cat_idx[obj_class]
                end_idx_out = cat_idx[obj_class+1]
                out_class_inds.append([begin_idx_out, end_idx_out-1])
        print("in_class: ", in_class)
        print("out_class: ", out_class_inds)
        cci = class_alignment(source_list, trial_list, in_class, out_class_inds)
        # Creates a list of out_class cci-scores per time unit
        for time, score in cci.items():
            if time not in ccis:
                ccis[time] = [score]
            else:  
                ccis[time].append(score)

    return ccis
        

def class_alignment(source_list, trial_list, in_class, out_class_inds):
    """
        This function computes the cci-value per object category. I
        structures MEG-data into responses per object class,
        and then computes the class response averages (centroids) for 
        parallelized PCA analysis.
        
        Parameters
        ----------
        source_list: spatiotemporal MEG-data with trial numbers in MNE format.
        trial_list: a list of trials coupled with the stimulus number.
        in_class: indices of the current category of interest.
        out_class: indices of the other categories to compare with.
    """
    
    import numpy as np
    from joblib import Parallel, delayed
    # Extract source estimate data, but save RAM by selecting in-class data only
    trials_ind= [idx for idx, trial in enumerate(trial_list) if trial >= in_class[0] and trial <= in_class[1]]

    # Pick the right indices for in_class data
    cond_data = [np.array(i.data) for i in np.array(source_list)[trials_ind]]# unnecessary?
    cond_data_out = [np.array(i.data) for i in source_list]
    # n_components for in-class PCA.
    n_comp = 1
    
    # Extracts normalized response matrix for in-class.
    exvar_in = exemp_var(trial_list, trials_ind, in_class, cond_data, source_list)
    # Creates in-class centroids per time step
    # (TO-DO:) Shouldnt we parallelize this computing step? Probably.
    in_class_centroids = {}
    for time in exvar_in:
        in_class_centroids[time] = [np.mean(np.array(exvar_in[time][cond]), axis=0) for cond in exvar_in[time]]
    
    # Compute out-class centroids per class per time step.
    out_class_centroids = {}
    # for every object class, extract MEG-responses and compute centroids per time step.
    for oc in out_class_inds:
        print("Loading out-class data for class indices: ", oc)
        trials_out= [idx for idx, trial in enumerate(trial_list) if trial >= oc[0] and trial <= oc[1]]
        exvar_out = exemp_var(trial_list, trials_out, oc, cond_data_out, source_list)
        out_centroid = {}
        
        # for every time step, create out-class centroids
        for time in exvar_out:
            out_centroid[time] = [np.mean(np.array(exvar_out[time][cond]), axis=0) for cond in exvar_out[time]]
        class_name = str(oc[0]) + "," + str(oc[1])
        out_class_centroids[class_name] = out_centroid
        
    # contrast in-class against all other classes distributed over all time points
    cci_time_tuple = Parallel(n_jobs=-1, verbose=5)(delayed(distr_cci_computation)
    (time = time, exemplar_vars=stimuli, out_class_centroids = out_class_centroids, in_class_centroids = in_class_centroids, n_comp=n_comp) 
    for time,stimuli in exvar_in.items())
    
    results = {}
    for time, cci_values in cci_time_tuple:
        results[time] = cci_values
        
    return results


def exemp_var(trial_list, trials_idx, ind_class, cond_data, source_list):
    """
        Extracts response matrices and converts them into dictionary format.
        
        Parameters
        ----------
        trial_list: a list of trials coupled with the stimulus number.
        trials_idx: set of indices that denotes out-class boundaries.
        ind_class: in-class indices.
        cond_data: relevant stimulus information.
        source_list: relevent MEG-data.
    """
    
    z_data = {}
    times = source_list[0].times
    # for every time step, map responses to the associated objects in a dictionary.
    for time_idx, time_step in enumerate(times):
        if time_step not in z_data:
                z_data[time_step] = {}
        for trial_idx, trial in enumerate(trials_idx):
            condition = trial_list[trial]
            
            # only include responses if trials are within current object boundaries
            if condition >= ind_class[0] and condition <= ind_class[1]:
                trial = cond_data[trial_idx]
                # extract all time points within a trial
                time_data = [t[time_idx] for t in trial]
                
                # for every time step, for every object, select data
                if condition not in z_data[time_step]:
                    z_data[time_step][condition] = [time_data]
                else: z_data[time_step][condition].append(time_data)
    return z_data


def distr_cci_computation(time, exemplar_vars, out_class_centroids, in_class_centroids, n_comp):
    """
        Distributes computation resources by parallelizing shared variance
        computation per time step.
        
        Parameters
        ----------
        time: the current time step in milliseconds.
        exemplar_vars: all selected MEG-data in dictionary format.
        out_class_centroids: computed object class response averages per out-class.
        in_class_centroids: computed object class response averages per in-class.
        n_comp: amount of principal components to use.
    """
    
    import numpy as np
        
    in_var = class_var(exemplar_vars, np.array(in_class_centroids[time]), n_comp)
#    print("in_var: ", in_var)
    
    # only compute cci for out_class
    out_vars = []
    for out_class in out_class_centroids:
        out_var = class_var(exemplar_vars, np.array(out_class_centroids[out_class][time]), n_comp)
        out_vars.append(out_var)
    cci = [in_var,out_vars]
    print("For this time point, the cci is: ", in_var/np.mean(out_vars))
    return [time,cci]
        

def class_var(ex_vars, data_centroids, n_comp):
    """
        Computes shared variance between centroids and response variance.
        
        Parameters
        ----------
        ex_vars: response variance for every object in the current in-class.
        data_centroids: response average for the current object class.
        n_comp: amount of principal components to use.
    """
    
    import numpy as np
    from sklearn.decomposition import PCA
    
    pca = PCA(n_components = 1)
    class_pca = pca.fit(data_centroids)
    # contrast every object response matrix against the current out-class.
    cci_values = {}
    for cond, zeta in ex_vars.items():
        class_pca.transform(np.array(zeta))
        cci_values[cond] = np.var(zeta)
    
    print("We computed the cci for one category for this many objects: ", len(list(cci_values.values())))
    return np.mean(list(cci_values.values()))


# compute Principal Component Analysis 'by hand' to allow rotation around axis.
#def compute_ci(exemplar_var, inclass_PCA, n_comp):
#    import numpy as np
#    from numpy import mean
#
#    # prepare exemplar variance to be transformed by in-class pca
#    prep = mean(exemplar_var.T, axis=1)
#    # center columns by subtracting column means
#    pre_trans = exemplar_var - prep #maakt dit uit?
#    # transform exemplar variance with class PC
#    trans_space = np.array(inclass_PCA.T.dot(pre_trans.T))
#    # calculate variance explained by class PC
#    ci = sum([np.var(trans_space[i]) for i in range(n_comp)])
#    return ci