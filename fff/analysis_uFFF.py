#!/usr/bin/env python

import numpy as np
import os as os
import bz2  as bz2 
import pandas as pd
import StringIO as StringIO
import matplotlib.pyplot as plt
import sys as sys

#Import 
#Author: Daniel-Adriano Silva

class ProgressBar():
	#http://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
    DEFAULT_BAR_LENGTH = float(65)

    def __init__(self, end, start=0):
        self.end    = end
        self.start  = start
        self._barLength = ProgressBar.DEFAULT_BAR_LENGTH

        self.setLevel(self.start)
        self._plotted = False

    def setLevel(self, level, initial=False):
        self._level = level
        if level < self.start:  self._level = self.start
        if level > self.end:    self._level = self.end

        self._ratio = float(self._level - self.start) / float(self.end - self.start)
        self._levelChars = int(self._ratio * self._barLength)

    def plotProgress(self):
        sys.stdout.write("\r  %3i%% [%s%s]" %(
            int(self._ratio * 100.0),
            '=' * int(self._levelChars),
            ' ' * int(self._barLength - self._levelChars),
        ))
        sys.stdout.flush()
        self._plotted = True

    def setAndPlot(self, level):
        oldChars = self._levelChars
        self.setLevel(level)
        if (not self._plotted) or (oldChars != self._levelChars):
            self.plotProgress()

    def __del__(self):
        sys.stdout.write("\n")

def plot_abinitio_vs_relax_energy_landscape(abinitio_rmsds_vs_scores=None, 
											relax_rmsds_vs_scores=None,
											binned_best_points_array=None,
											plot_title="",
											xlimits=[0.0, 8.0],
											ylimits=[-2.2, -1.0],
											out_plot_name=""):
	fig = plt.figure(figsize=(15,10))
	ax = fig.add_subplot(2,2,1)
	#plot data 
	ax.scatter(abinitio_rmsds_vs_scores[:,0], abinitio_rmsds_vs_scores[:,1], c='red', marker='o', s=25)
	#print relax_rmsds, relax_scores
	ax.scatter(relax_rmsds_vs_scores[:,0], relax_rmsds_vs_scores[:,1], c='blue', marker='o', s=60)
	if len(binned_best_points_array) > 0:
		ax.scatter(binned_best_points_array[:,0], binned_best_points_array[:,1], c='orange', marker='o', s=100)
	ax.set_title("FFFplot %s"%plot_title)
	ax.set_xlabel('RMSD (A)')
	ax.set_ylabel('Score per res')
	##ax.set_yscale('log')
	ax.set_xlim(xlimits)
	ax.set_ylim(ylimits)
	
	if len(out_plot_name) > 0:
		fig.savefig(out_plot_name)  
	plt.close('all')


def evaluate_FFEL(abinitio_rms_vs_score=None,
				  relax_rms_vs_score=None,
				  relax_rms_limit=0.3,
				  relax_rms_dispersion_limit=0.2,
				  relax_energy_limit=-1.7,
				  relax_energy_dispersion_limit=0.3,
				  abinitio_histogram_bins=np.arange(0, 5.1, 0.5),
				  number_of_min_energy_points_for_eval=5,
				  min_number_of_samples_per_bin=3,
				  abinitio_minimum_sampled_distance_threshold=1.0,
				  abinitio_minimum_sampled_energy_to_relax_threshold=0.2,
				  abinitio_zeroEnergy_tolerance_threshold_distance=1.0,
				  abinitio_funnel_decay_tolerance=0.1,
				  distance_to_evaluate_funnel_decay=3.0,
				  accepted_energy_gap_from_relax=0.3,
				  distance_to_evaluate_energy_gap=3.0,
				  minimum_energy_gap_abinitio_funnel=0.1,
				  min_density_of_abinitio_rms_nearest_points=0.1,
				  distance_threshold_for_abinitio_rms_nearest_points=1.5,
				  b_fast_mode=False,
				  b_debug=False):
	
	pass_test=True
	comments_out=[]
			
	#Evaluate the FF EL
	# 0 is rms, 1 is energy
	rmsd_ndx=0
	energy_ndx=1
	stddev_ndx=2
	#First check the relax structure
	relax_rmsd_avg=np.average(relax_rms_vs_score[:,rmsd_ndx])
	relax_energy_avg=np.average(relax_rms_vs_score[:,energy_ndx])
	if (   relax_rmsd_avg >= relax_rms_limit ):
		pass_test=False
		comments_out.append("RelaxRMSDLimit")
	if ( np.std(relax_rms_vs_score[:,rmsd_ndx]) >= relax_rms_dispersion_limit ):
		pass_test=False
		comments_out.append("RelaxRMSDStdDev")
	if ( relax_energy_avg >= relax_energy_limit ):
		pass_test=False
		comments_out.append("RelaxEnerLimit")
	elif ( np.std(relax_rms_vs_score[:,energy_ndx]) >= relax_energy_dispersion_limit ):
		pass_test=False
		comments_out.append("RelaxEnerStdDev")
	
	#Calculate the best X energy points by RMSD bins
	avg_binned_best_points_array=[] #np.zeros((len(abinitio_histogram_bins),number_of_min_energy_points_for_eval),float)
	for i in xrange(len(abinitio_histogram_bins)-1): 
		tmp_bitmask=((abinitio_rms_vs_score[:,rmsd_ndx] >= abinitio_histogram_bins[i]) * 
										   (abinitio_rms_vs_score[:,rmsd_ndx] < abinitio_histogram_bins[i+1]))
		#Extract best 5 points
		sortedbinpoints_ndx=np.argsort(abinitio_rms_vs_score[tmp_bitmask][:,1])
		bin_counts=len(sortedbinpoints_ndx)
		bestfivepoints_ndx=sortedbinpoints_ndx[0:number_of_min_energy_points_for_eval]
		bestfivepoints=abinitio_rms_vs_score[tmp_bitmask][bestfivepoints_ndx]
		if (len(bestfivepoints) >= min(min_number_of_samples_per_bin,number_of_min_energy_points_for_eval)):
			#If there is data add the average to the result array
			avg_binned_best_points_array.append([(np.average(bestfivepoints[:,0])), 
									  np.average(bestfivepoints[:,1]), np.std(bestfivepoints[:,1]), float(bin_counts)])
			
	#For the last bin (i.e. > largest-value) Calculate the best 5 energy points by RMSD bins
	tmp_bitmask=((abinitio_rms_vs_score[:,rmsd_ndx] >= abinitio_histogram_bins[-1]))
	#Extract best 5 points
	sortedbinpoints_ndx=np.argsort(abinitio_rms_vs_score[tmp_bitmask][:,1])
	bin_counts=len(sortedbinpoints_ndx)
	bestfivepoints_ndx=sortedbinpoints_ndx[0:number_of_min_energy_points_for_eval]
	bestfivepoints=abinitio_rms_vs_score[tmp_bitmask][bestfivepoints_ndx]
	if (len(bestfivepoints) > min(min_number_of_samples_per_bin,number_of_min_energy_points_for_eval)):
		#If there is data add the average to the result array
		avg_binned_best_points_array.append([(np.average(bestfivepoints[:,0])), 
								  np.average(bestfivepoints[:,1]), np.std(bestfivepoints[:,1]), float(bin_counts)])
	avg_binned_best_points_array=np.asarray(avg_binned_best_points_array, float) 
	
	#Now use the binned points to check what follows:
	#Evaluate Abinitio
	##1. See if the nearest point is near enough
	if (avg_binned_best_points_array[0][rmsd_ndx] > abinitio_minimum_sampled_distance_threshold):
		pass_test=False
		comments_out.append("MinAbinitioDistance")
		if b_fast_mode:
			return pass_test, comments_out, avg_binned_best_points_array
	##2. Check that the energy of the neares point sampled is near enough
	if (abs(avg_binned_best_points_array[0][energy_ndx]-
			relax_energy_avg) >  abinitio_minimum_sampled_energy_to_relax_threshold):
		pass_test=False
		comments_out.append("AbinitioEnergyToHigh")
		if b_fast_mode:
			return pass_test, comments_out, avg_binned_best_points_array
	##3. See that no point beyond some threshold is lower in energy than the relax
	abinitio_major_than_threshold_ndx = np.where(
							avg_binned_best_points_array[:,rmsd_ndx]>
							abinitio_zeroEnergy_tolerance_threshold_distance)[0]
	for indx in abinitio_major_than_threshold_ndx:
		#0 is RMSD, 1 
		if (avg_binned_best_points_array[indx][energy_ndx] < (relax_energy_avg-
															abinitio_minimum_sampled_energy_to_relax_threshold)):
			pass_test=False
			comments_out.append("MuchLowerEnergyThanRelax")
			if b_fast_mode:
				return pass_test, comments_out, avg_binned_best_points_array
			break
			
	##4. Now check that points always grow or mantain ~flat up to the last bin
	max_ener_observed=avg_binned_best_points_array[0][energy_ndx] 
	for indx in xrange(len(avg_binned_best_points_array)-1):
		if (avg_binned_best_points_array[indx][energy_ndx] > max_ener_observed):
			max_ener_observed=avg_binned_best_points_array[indx][energy_ndx]
			###if ( max_ener_observed > (relax_energy_avg+accepted_energy_gap_from_relax ) ):
			##max_ener_observed=relax_energy_avg+accepted_energy_gap_from_relax
		#Evaluate this only if the destance to evaluate is correct (i.e. < than certain threshold)
		if(avg_binned_best_points_array[indx][rmsd_ndx] <= distance_to_evaluate_funnel_decay):
			#if ( (avg_binned_best_points_array[indx+1][energy_ndx]-
			#	  avg_binned_best_points_array[indx+1][stddev_ndx]) < (max_ener_observed - abs(max_ener_observed*
			#																			   abinitio_funnel_decay_tolerance))
			#	):
			if ( (avg_binned_best_points_array[indx+1][energy_ndx]) < (max_ener_observed - abs(max_ener_observed*
																						   abinitio_funnel_decay_tolerance))  
				):
				pass_test=False
				comments_out.append("BadFunnelShape")
				if b_fast_mode:
					return pass_test, comments_out, avg_binned_best_points_array
				break
	
	#Check that the energy gap exist
	if (len(avg_binned_best_points_array) > 1):
		if(avg_binned_best_points_array[-1][rmsd_ndx] > distance_to_evaluate_energy_gap):
			if( (avg_binned_best_points_array[-1][energy_ndx]-
				 relax_energy_avg ) < minimum_energy_gap_abinitio_funnel):
				pass_test=False
				comments_out.append("BadEnergyGap")
				if b_fast_mode:
					return pass_test, comments_out, avg_binned_best_points_array
				
	
	#Finally check the density of the points near to the relax state
	tmp_near_ndxs=np.where(avg_binned_best_points_array[:,0]<=distance_threshold_for_abinitio_rms_nearest_points)
	tmp_density_of_near_abinitio_points=avg_binned_best_points_array[tmp_near_ndxs,3].sum()/avg_binned_best_points_array[:,3].sum()
	if (tmp_density_of_near_abinitio_points < min_density_of_abinitio_rms_nearest_points):
		pass_test=False
		comments_out.append("LowAbinitioDensityNearRelax")
		if b_fast_mode:
			return pass_test, comments_out, avg_binned_best_points_array
	
	return pass_test, comments_out, avg_binned_best_points_array #, difference_abinitio_from_relax
	

b_ralph=False

root_job_path="./"

jobdata_file="%s/boinc_job_names.dat"%(root_job_path)
job_id_file="%s/boinc_job_id.dat"%(root_job_path)

analysis_results_path="%s/analysis"%root_job_path
analysis_results_path_good="%s/pass"%analysis_results_path
analysis_results_path_bad="%s/fail"%analysis_results_path

#Read the information of the Job IDs
jobdata_dic = {}
for jobdata in file(jobdata_file):
	jobdata=jobdata.strip().split()
	if not jobdata[0] in jobdata_dic:
		jobdata_dic[jobdata[0]]=[ jobdata[1], jobdata[2] , jobdata[3] ]
	else:
		print "ERROR, repeated job!!! listed:", jobdata[0]
		assert 0==1
		
job_id=int(file(job_id_file).readline())

print "Jobs in list: ", len(jobdata_dic)



#Create dirs
print "Results will be output to: "
d = analysis_results_path
print d
if not os.path.exists(d):
	try:
		os.makedirs(d)
	except:
		print "Can't create output Dir"
	
d = analysis_results_path_good
print d
if not os.path.exists(d):
	try:
		os.makedirs(d)
	except:
		print "Can't create output Dir"

d = analysis_results_path_bad
print d
if not os.path.exists(d):
	try:
		os.makedirs(d)
	except:
		print "Can't create output Dir"
	

#Now analyse the data
idata_counter=0
idata_exist_counter=0
goodFFs_list=[]
badFFs_list=[]


print "Be patient, now I'll analyze your data."
pb = ProgressBar(len(jobdata_dic))
f_pass = open("%s/analysis_passFFF.dat"%analysis_results_path, 'w')
f_fail = open("%s/analysis_failFFF.dat"%analysis_results_path, 'w')
for idata in jobdata_dic:
	idata_counter+=1
	
	if ( idata_counter%100 == 0):
		pb.setAndPlot(idata_counter)
	
	idata_seq_ndx=0
	idata_pathname_ndx=1
	idata_pdbname_ndx=2

	abinitio_file=""
	relax_file=""
	
	if not b_ralph:
		abinitio_file="/net/BOINC/results/%s/%s_abinitio_SAVE_ALL_OUT_%d_0.all.out.bz2"%(idata[0:8], 
																						 idata, 
																						 job_id)
		relax_file="/net/BOINC/results/%s/%s_relax_SAVE_ALL_OUT_%d_0.all.out.bz2"%(idata[0:8], 
																				   idata, 
																				   job_id)

	else:
		abinitio_file="/net/RALPH/results/%s/%s_abinitio_SAVE_ALL_OUT_%d_0.all.out.bz2"%(idata[0:8], 
																						 idata, 
																						 job_id)
		relax_file="/net/RALPH/results/%s/%s_relax_SAVE_ALL_OUT_%d_0.all.out.bz2"%(idata[0:8], 
																				   idata, 
																				   job_id)
	if ( os.path.isfile(abinitio_file) and os.path.isfile(relax_file)):
		idata_exist_counter+=1
		#Read abinitio
		"""
		abinitio_data_array=[]
		print bz2.BZ2File(relax_file).read()
		is_first=True
		break
		for line in StringIO(bz2.BZ2File(relax_file).read()):
			line=line.strip().split()
			if(line[0:6]=="SCORE:"):
				abinitio_data_array.append()
		break
		"""
		abinitio_df=pd.read_csv(StringIO.StringIO(bz2.BZ2File(abinitio_file).read()), delim_whitespace=True)
		relax_df=pd.read_csv(StringIO.StringIO(bz2.BZ2File(relax_file).read()), delim_whitespace=True)
		
		#Convert to np
		seq_len=float(len(jobdata_dic[idata][idata_seq_ndx]))
		#Get relevan data
		good_ndx_abinitio=np.where(abinitio_df.iloc[:,0].values == "SCORE:")[0]
		good_ndx_relax=np.where(relax_df.iloc[:,0].values == "SCORE:")[0]
		#Check that we have enough data to see somthing
		if (len(good_ndx_abinitio) < 10) or (len(good_ndx_relax) < 10):
			continue
		#Abinitio: Score normalized by seq_len
		abinitio_rms_vs_score=np.zeros((len(good_ndx_abinitio),2), float)
		abinitio_rms_vs_score[:,0]=abinitio_df['rms'].values[good_ndx_abinitio].astype(float)
		abinitio_rms_vs_score[:,1]=abinitio_df['score'].values[good_ndx_abinitio].astype(float)/seq_len
		#Relax: Score normalized by seq_len
		relax_rms_vs_score=np.zeros((len(good_ndx_relax),2), float)
		relax_rms_vs_score[:,0]=relax_df['rms'].values[good_ndx_relax].astype(float)
		relax_rms_vs_score[:,1]=relax_df['score'].values[good_ndx_relax].astype(float)/seq_len
		
		
		#Evaluate the FFfunnel
		#ToDo: 
		#  1. Document this with detail!
		b_is_good, ff_analysis_failure_comments, avg_binned_best_points_array=evaluate_FFEL(
				  abinitio_rms_vs_score=abinitio_rms_vs_score,
				  relax_rms_vs_score=relax_rms_vs_score,
				  relax_rms_limit=1.5,
				  relax_rms_dispersion_limit=0.5,
				  relax_energy_limit=-1.40,
				  relax_energy_dispersion_limit=0.5,
				  abinitio_histogram_bins=np.arange(0.0, 6.0, 1.0),
				  number_of_min_energy_points_for_eval=5,
				  min_number_of_samples_per_bin=3,
				  abinitio_minimum_sampled_distance_threshold=1.5,
				  abinitio_minimum_sampled_energy_to_relax_threshold=0.2,
				  abinitio_zeroEnergy_tolerance_threshold_distance=1.0, 
				  abinitio_funnel_decay_tolerance=0.02, #0.01
				  distance_to_evaluate_funnel_decay=3.0,
				  accepted_energy_gap_from_relax=0.3, #0.2
				  distance_to_evaluate_energy_gap=4.0,
				  minimum_energy_gap_abinitio_funnel=0.1,
				  min_density_of_abinitio_rms_nearest_points=0.1, #float(0.0-1.0) Minimum abinitio point density near to relax 
				  distance_threshold_for_abinitio_rms_nearest_points=2.5, #float(>0.0) Distance threshold to calculate abinitio density
				  b_fast_mode=True,
				  b_debug=False)
		
		if b_is_good:
			goodFFs_list.append(jobdata_dic[idata][idata_pathname_ndx])
			tmp_title=jobdata_dic[idata][idata_pathname_ndx]
			f_pass.write("%s"%idata)
			f_pass.write("\t%s"%tmp_title)
			tmp_title_splitByChar=list(tmp_title)
			max_line_len = 80
			tmp_title_join=[''.join(tmp_title_splitByChar[x:x+max_line_len]) for x in xrange(0, len(tmp_title_splitByChar), max_line_len)]
			tmp_title=""
			for i in tmp_title_join:
				tmp_title+=i+"\n"
			plot_abinitio_vs_relax_energy_landscape( abinitio_rms_vs_score,
												relax_rms_vs_score,
												avg_binned_best_points_array,
												plot_title=tmp_title,
												xlimits=[-0.1, 8.0],
												ylimits=[(min(-1.7,
															 min(abinitio_rms_vs_score[:,1].min(),
																 relax_rms_vs_score[:,1].min()))-0.05 ), 
														 -1.3],
												out_plot_name="%s/%s.png"%(analysis_results_path_good,
																	  idata))
			f_pass.write("\n")
		else:
			badFFs_list.append(jobdata_dic[idata][idata_pathname_ndx])
			tmp_title=jobdata_dic[idata][idata_pathname_ndx]
			f_fail.write("%s"%idata)
			f_fail.write("\t%s"%tmp_title)
			tmp_title_splitByChar=list(tmp_title)
			max_line_len = 80
			tmp_title_join=[''.join(tmp_title_splitByChar[x:x+max_line_len]) for x in xrange(0, len(tmp_title_splitByChar), max_line_len)]
			tmp_title=""
			for i in tmp_title_join:
				tmp_title+=i+"\n"
			for icomment in ff_analysis_failure_comments:
				tmp_title=tmp_title+icomment+", "
				f_fail.write("\t%s"%icomment)
			plot_abinitio_vs_relax_energy_landscape( abinitio_rms_vs_score,
												relax_rms_vs_score,
												avg_binned_best_points_array,
												plot_title=tmp_title,
												xlimits=[-0.1, 8.0],
												ylimits=[(min(-1.7,
															 min(abinitio_rms_vs_score[:,1].min(),
																 relax_rms_vs_score[:,1].min()))-0.05 ), 
														 -1.3],
												out_plot_name="%s/%s.png"%(analysis_results_path_bad,
																	  idata))
			f_fail.write("\n")
f_pass.close()
f_pass.close()
del pb
print "Total number of jobs analyzed: ", idata_counter
print "Total number of jobs with complete data (abinitio&relax):", len(goodFFs_list)+len(badFFs_list)

if ( (len(goodFFs_list)+len(badFFs_list)) > 0 ):
	print "Total number of jobs with good FFF funnels: ", len(goodFFs_list)
	if (len(goodFFs_list) > 0):
		print "Good FFF list: "
		for iname in goodFFs_list:
			print iname
	else:
		print "Well... Not a single job with good FFF was found. What is wrong with your designs pal?"
		
print "All Done"





