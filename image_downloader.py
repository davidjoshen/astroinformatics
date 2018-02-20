import numpy as np
import pandas as pd
import pyvo as vo
import os
from astropy.io import fits

'''----------------------------------HAVE TO DO WITH THE CODE--------------------------------------
-Have to pass arguments into the code example what survey you want to download your data from
-Parameters abount the quesy size
-The query format
-The number of image to be downloaded from the database file, etc ...
-Where image files should be downloaded
---------------------------------------------------------------------------------------------------
'''

data=pd.read_csv("galaxy_sur_main.csv",sep=',')
pos=(2,)

''' This is for NVSS
if not os.path.exists("NVSS2"):
    os.mkdir("NVSS2")
if not os.path.exists("NVSSimages_final"):
    os.mkdir("NVSSimages_final")
'''
if not os.path.exists("SUMSS2"):
    os.mkdir("SUMSS2")
if not os.path.exists("SUMSSimages_final"):
    os.mkdir("SUMSSimages_final")
    
# setup a query object for NVSS
#nvss = "http://skyview.gsfc.nasa.gov/cgi-bin/vo/sia.pl?survey=nvss&"
sumss = "http://skyview.gsfc.nasa.gov/cgi-bin/vo/sia.pl?survey=sumss&"
#query = vo.sia.SIAQuery(nvss)
query = vo.sia.SIAQuery(sumss)
query.size = 0.5                 # degrees
query.format = 'image/fits'


for n in range(0, 575):
	try:
          if (data['dec'][n]<-40.0):
		pos=(data['ra'][n],data['dec'][n])
		name=data['NED_id'][n]
		#fits_util.cut_out(RA,DEC,name)
		query.pos = pos
		results=query.execute()
    		for image in results:        	    
                        print "Downloading %s..." % name
        		image.cachedataset(filename="SUMSS2/%s.fits" % name)
		data_2, header = fits.getdata('SUMSS2/'+name+'.fits',header=True)
		header['l']=data['l'][n]
		header['b']=data['b'][n]
		header['Kmag']=data['Kmag'][n]
		header['Kmag_err']=data['Kmag_err'][n]
		header['z']=data['z'][n]
		header['zdist']=data['zdist'][n]		
		header['D']=data['D'][n]
		header['D_err']=data['D_err'][n]
		header['gal_type']=data['gal_type'][n]
		header['n_sumss']=data['n_sumss'][n]
		header['F1400']=data['F1400'][n]
		header['F1400_err']=data['F1400_err'][n]
		header['F843']=data['F843'][n]
		header['F843_err']=data['F843_err'][n]
		header['2MASX']=data['2MASX'][n]
		header['class']=data['class'][n]
		header['BMIN']=0.0125
		header['BMAJ']=0.0125
		header['BPA']=0.0
        
		fits.writeto('SUMSSimages_final/'+name+'.fits', data_2, header,clobber=True)

	except IOError:
		print 'Hahaha this one is out of range :P this one you ll never get '+name

	



