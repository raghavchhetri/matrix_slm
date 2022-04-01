import numpy as np
from matrixpack.constants import dx, dz, MagAM, fSLM, SLMpixel, SLMheight, SLMwidth, beamD
from LightPipes import um, nm, Begin, GaussBeam, RectAperture

def tar(movebeams_um=[0,0,0,0,0,0,0,0,0], tag='MATRIX'):
    #(+ve values for `movebeams_um` moves the beam UP in sample space i.e., along +Z in the microscope)
    
    wavelength_min = 488*nm
    
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
        movetag = '_far'+str(movebeams_um[0])+'.'+str(movebeams_um[3])+'.'+str(movebeams_um[6])+ \
        '_mid'+str(movebeams_um[1])+'.'+str(movebeams_um[4])+'.'+str(movebeams_um[7])+ \
        '_near'+str(movebeams_um[2])+'.'+str(movebeams_um[5])+'.'+str(movebeams_um[8])+'.bmp'
            
# Grid for the computation of the optical fields
    gridsize = np.ceil((fSLM*wavelength_min/SLMpixel)/dZ)*dZ

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
    print('SLM sufficiently sampled: PROCEED. \n') if gridpixels > SLMheight else print('WARNING: SLM undersampled. Check "Nunits" in `target_pattern` \n')

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
    Field= Begin(gridsize, wavelength_min, gridpixels) #Plane wave distribution with amplitude 1 and phase 0
    Field= GaussBeam(Field, beamD/2)
    SLMfield = RectAperture(Field, sx=SLMheight*SLMpixel, sy=SLMwidth*SLMpixel, x_shift=0.0, y_shift=0.0, angle=0.0)
    print('Input Field on the SLM:')
    print(type(SLMfield.field), SLMfield.field.dtype, SLMfield.field.shape, '\n')
    
# Target pattern
    target = np.zeros((gridpixels, gridpixels)) #Note: LightPipes command 'SubIntensity' needs floats
    for j in range(len(spots_X)):
        target[spots_X[j],spots_Z[j]] = 255
    print('Target Field Intensity:')
    print(type(target), target.shape, np.min(target), np.max(target), target.dtype)    

    return SLMfield, target, movetag

if __name__ == '__main__':
    tar()