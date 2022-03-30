import time
import numpy as np
import pylab as plt
from skimage import io
from os.path import join
from LightPipes import PipFFT, SubIntensity, Phase, um, nm, Begin, GaussBeam, RectAperture

def target_pattern(wavelength,beamD,fSLM,SLMpixel,SLMwidth,SLMheight,dx,dz,MagAM,tag='MATRIX',movebeams_um=[0,0,0,0,0,0,0,0,0]):
#(+ve values for `movebeams_um` moves the beam UP in sample space i.e., along +Z in the microscope)

# X-separation in space space between beams on the same focal plane 
    sepx  = 4*dz 

# Beam Spacing at the Apodizing Mask
    dX = MagAM*dx 
    dZ = MagAM*dz 
    sepX = MagAM*sepx 

# Shift Beams at the Apodizing Masks
    #far beams
    move_beam1 = MagAM*movebeams_um[0]*um
    move_beam4 = MagAM*movebeams_um[3]*um
    move_beam7 = MagAM*movebeams_um[6]*um

    #mid beams
    move_beam2 = MagAM*movebeams_um[1]*um
    move_beam5 = MagAM*movebeams_um[4]*um
    move_beam8 = MagAM*movebeams_um[7]*um

    #near beams
    move_beam3 = MagAM*movebeams_um[2]*um
    move_beam6 = MagAM*movebeams_um[5]*um
    move_beam9 = MagAM*movebeams_um[8]*um
    
    if movebeams_um==[0,0,0,0,0,0,0,0,0]:
        movetag = '.bmp'
    else:       
        movetag = '-[f147-'+str(movebeams_um[0])+'.'+str(movebeams_um[3])+'.'+str(movebeams_um[6])+ \
        ']-[m258-'+str(movebeams_um[1])+'.'+str(movebeams_um[4])+'.'+str(movebeams_um[7])+ \
        ']-[n369_'+str(movebeams_um[2])+'.'+str(movebeams_um[5])+'.'+str(movebeams_um[8])+'].bmp'
            
# Grid for the computation of the optical fields
    gridsize = np.ceil((fSLM*wavelength/SLMpixel)/dZ)*dZ

# Optic axis co-ordinate(zero-order beam)
    Oaxis = gridsize/2

# Define center beam (beam5) position in the 3x3 array
    X = Oaxis
    Z = Oaxis - 2*dZ

# Choose Nunits 'Number of grid-units per dZ' such that gridpixels > SLMheight
#Note: Pick Nunits such that mod(dZ=420,Nunits) = 0, Eg: [20,30,60,70,140,210]
    Nunits = 70; #For 488, 30 and up; For 561/631, 20 and up
    unit = dZ/Nunits
    gridpixels = int(gridsize/unit)
    print('Pixels in the grid:', gridpixels)
    print('Pixels along SLM height:',SLMheight)
    print('SLM sufficiently sampled: PROCEED.') if gridpixels > SLMheight else print('WARNING: SLM undersampled. Check "Nunits" in `target_pattern`')

# Define beam-spot positions at the Apodizing Mask
    if tag == 'MATRIX': # 3 x 3 Beams
        spots_X = np.array([(X-dX)-sepX, X-sepX, (X+dX)-sepX,
                            (X-dX), X, (X+dX),
                            (X-dX)+sepX, X+sepX, (X+dX)+sepX])/unit
        spots_Z = np.array([Z-dZ+move_beam1, Z+move_beam2, Z+dZ+move_beam3,
                            Z-dZ+move_beam4, Z+move_beam5, Z+dZ+move_beam6,
                            Z-dZ+move_beam7, Z+move_beam8, Z+dZ+move_beam9])/unit

    elif tag == 'NEAR': #Beams-3-6-9
        spots_X = np.array([(X+dX)-sepX, X+dX, (X+dX)+sepX])/unit
        spots_Z = np.array([Z+dZ+move_beam3, Z+dZ+move_beam6, Z+dZ+move_beam9])/unit

    elif tag == 'NEAR_beam3':
        spots_X = np.array([(X+dX)-sepX])/unit
        spots_Z = np.array([Z+dZ+move_beam3])/unit

    elif tag == 'NEAR_beam6':
        spots_X = np.array([X+dX])/unit
        spots_Z = np.array([Z+dZ+move_beam6])/unit

    elif tag == 'NEAR_beam9':
        spots_X = np.array([(X+dX)+sepX])/unit
        spots_Z = np.array([Z+dZ+move_beam9])/unit

    elif tag == 'MID': #Beams-2-5-8
        spots_X = np.array([X-sepX, X, X+sepX])/unit
        spots_Z = np.array([Z+move_beam2, Z+move_beam5, Z+move_beam8])/unit

    elif tag == 'MID_beam2':
        spots_X = np.array([X-sepX])/unit
        spots_Z = np.array([Z+move_beam2])/unit

    elif tag == 'MID_beam5':
        spots_X = np.array([X])/unit
        spots_Z = np.array([Z+move_beam5])/unit

    elif tag == 'MID_beam8':
        spots_X = np.array([X+sepX])/unit
        spots_Z = np.array([Z+move_beam8])/unit

    elif tag == 'FAR': #Beams-1-4-7
        spots_X = np.array([(X-dX)-sepX, X-dX, (X-dX)+sepX])/unit
        spots_Z = np.array([Z-dZ+move_beam1, Z-dZ+move_beam4, Z-dZ+move_beam7])/unit

    elif tag == 'FAR_beam1':
        spots_X = np.array([(X-dX)-sepX])/unit
        spots_Z = np.array([Z-dZ+move_beam1])/unit

    elif tag == 'FAR_beam4':
        spots_X = np.array([X-dX])/unit
        spots_Z = np.array([Z-dZ+move_beam4])/unit

    elif tag == 'FAR_beam7':
        spots_X = np.array([(X-dX)+sepX])/unit
        spots_Z = np.array([Z-dZ+move_beam7])/unit

    elif tag == 'DIAGONAL': #Beams-1-5-9
        spots_X = np.array([(X-dX)-sepX, X, (X+dX)+sepX])/unit
        spots_Z = np.array([Z-dZ+move_beam1, Z+move_beam5, Z+dZ+move_beam9])/unit

    spots_X = spots_X.astype(int)
    spots_Z = spots_Z.astype(int)

# Input field on the SLM    
    Field= Begin(gridsize, wavelength, gridpixels) #Plane wave distribution with amplitude 1 and phase 0
    Field= GaussBeam(Field, beamD/2)
    SLMfield = RectAperture(Field, sx=SLMheight*SLMpixel, sy=SLMwidth*SLMpixel, x_shift=0.0, y_shift=0.0, angle=0.0)
    print('Input Field on the SLM:')
    print(type(SLMfield.field), SLMfield.field.dtype, SLMfield.field.shape) 
    
# Target pattern
    target = np.zeros((gridpixels, gridpixels)) #Note: LightPipes command 'SubIntensity' needs floats
    for j in range(len(spots_X)):
        target[spots_X[j],spots_Z[j]] = 255
    print('Target Field Intensity:')
    print(type(target), target.shape, np.min(target), np.max(target), target.dtype)    

    return SLMfield, target, movetag


def generate_mask(wavelength, SLMfield, target, SLMwidth, SLMheight, outPath, footer, Niter = 12, tag = 'MATRIX'):
#Iteration loop to get phase distribution
    Field = SLMfield
    gridpixels = len(target) #same size as the Target
    UniformIntensity = np.ones((gridpixels, gridpixels)) #Matrix filled with 1's to substitute a uniform intensity profile

    t0 = time.time()
    for i in range(Niter):     
    #2-D Fourier transform of the field; Forward transform with index 1
        Field = PipFFT(Field, index = 1)     
    #Substitute the original intensity distribution while leaving the phase unchanged
        Field = SubIntensity(Field, target)
    #Inverse Fourier transform; Back transform with index -1
        Field = PipFFT(Field, index = -1) 
    #Substitute a uniform intensity while leaving the phase unchanged
        Field = SubIntensity(Field, UniformIntensity)
    print('Took', round(time.time()-t0,2), 'sec')

#Extract phase distribution from the field
    Phaze = Phase(Field) 
    PhaseZeroed = Phaze + np.abs(np.min(Phaze))

    # Convert to 8-bit
    Phase8 = PhaseZeroed*(255/np.max(PhaseZeroed))
    print(type(Phase8), Phase8.shape, Phase8.dtype)
    phaseMask8 = Phase8[0:SLMwidth,0:SLMheight].astype('uint8')
    print(type(phaseMask8), phaseMask8.shape, phaseMask8.dtype)

    fig = plt.figure(figsize=(10,6))
    io.imshow(phaseMask8); io.show()

#Save mask to be applied to SLM
    outfilename= str(int(wavelength/nm))+'nm_Niter'+str(Niter)+'_' +tag +footer
    io.imsave(join(outPath, outfilename), phaseMask8)
    
if __name__ == '__main__':
    target_pattern()
    generate_mask()