# matrix_slm
03-30-2022 
Raghav K. Chhetri

Gerchberg-Saxton algorithm to generate 3x3 beams for the Matrix microscope

### <code>GerchbergSaxton_Matrix.ipynb </code> 
    - Phase Retrievel via Gerchberg-Saxton algorithm to generate phase masks for an SLM 
    - Using "LightPipes for Python"
    
### Usage
---
    1. Define target pattern `target_pattern()`
    2. Compute phase mask to generate the above target pattern when applied to an SLM `generate_mask`
    3. Generated patterns are saved as .bmp in the masks folder. Load these onto the SLM
    
    Convention for `movebeams_um`

        movebeams_um=[beam1,beam2,beam3,
                      beam4,beam5,beam6,
                      beam7,beam8,beam9]
        where
        far = beams1-4-7
        mid = beams2-5-8
        near = beams3-6-9  
    +ve values for `movebeams_um` moves the beam UP in sample space i.e., along +Z in the microscope