## matrix_slm
Raghav K. Chhetri

Phase Retrievel via Gerchberg-Saxton algorithm to generate phase masks for use with Meadowlarks SLM HSP1920 in the Matrix microscope 

Using "LightPipes for Python"
    
### Usage
`GerchbergSaxton_Matrix.ipynb` which calls the following functions:
- `target_pattern()` to define target pattern. Available selections: 

    `MATRIX`
    
    `FAR`, `FAR_beam1`, `FAR_beam4`, `FAR_beam7`
    
    `MID`, `MID_beam2`, `MID_beam5`, `MID_beam8`
    
    `NEAR`, `NEAR_beam3`, `NEAR_beam6`, `NEAR_beam9`
    
    `DIAGONAL` i.e., beams 1-5-8

    It also allows the position of each beam to be shifted via `movebeams_um` parameter which follows this convention:

        movebeams_um = [beam1, beam2, beam3,
                        beam4, beam5, beam6,
                        beam7, beam8, beam9]
        where
        far = beams1-4-7
        mid = beams2-5-8
        near = beams3-6-9  
        
        Note: +ve values for `movebeams_um` moves the beam UP in sample space 
        i.e., along +Z in the Matrix microscope
        
- `generate_mask()`to compute phase mask to generate selected target pattern and save as .bmp to load onto the SLM
