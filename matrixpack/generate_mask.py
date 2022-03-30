import time
import numpy as np
import pylab as plt
from skimage import io
from os.path import join
from LightPipes import PipFFT, SubIntensity, Phase, nm

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
    generate_mask()