from LightPipes import um, mm

#Spatial offset of beams in sample plane
dx  = 75*um
dz = 70*um

#Magnification from sample to Apodizing Mask
MagAM = 6

fSLM = 750*mm
SLMpixel = 9.2*um
SLMheight = 1920
SLMwidth = 1152

 #1/e diameter on the SLM = 1.2 x FWHM_width
beamD = 1.2*9*mm