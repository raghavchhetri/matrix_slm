## matrix_slm
Raghav K. Chhetri

Phase Retrievel via Gerchberg-Saxton algorithm to generate phase masks for Meadowlarks HSP1920 SLM in the Matrix microscope 

Using "LightPipes for Python"
    
### Usage
1. To generate a small number of user-defined patterns, use `GerchbergSaxton_Matrix.ipynb`. It calls the following modules:

    a. `target_pattern()` to define target pattern. Available selections are as follows-

    `MATRIX`
    
    `FAR`, `FAR_beam1`, `FAR_beam4`, `FAR_beam7`
    
    `MID`, `MID_beam2`, `MID_beam5`, `MID_beam8`
    
    `NEAR`, `NEAR_beam3`, `NEAR_beam6`, `NEAR_beam9`
    
    `DIAGONAL` i.e., beams 1-5-9

    It also allows the position of each beam to be manually defined via the `movebeams_um` parameter, which follows this convention-

        movebeams_um = [beam1, beam2, beam3,
                        beam4, beam5, beam6,
                        beam7, beam8, beam9]
        where
        far = beams1-4-7
        mid = beams2-5-8
        near = beams3-6-9  
        
        Note: +ve values for `movebeams_um` moves the beam UP in sample space 
        i.e., along +Z in the Matrix microscope       
    
    b. `generate_mask()`to compute phase mask as .bmp, which when applied to the SLM generates its corresponding target pattern
    
    -----
2. To generate a large batch of patterns for a grid of beam positions (see rules below), use `GerchbergSaxton_Matrix_MultiProcess.ipynb`. It calls the following modules:

    a. `move_func()` to auto-generate a list of beam positions to run multiprocessing on
    
    b. `mask_func()` to compute phase mask for each beam position. 
    
    c. `target_func()` to define target pattern for each beam position. All above target pattern selections are available
    
       Rules for beam positions on a 3x3 grid:
       - Each beam has two choices: 0 or +step, then 2^9 = 512 combinations
       - Each beam has two choices: 0 or -step (511 combinations: all zeros is already counted)
       - Each beam has two choices: +step or -step (510 combinations: all +step and all -step already counted)
       So, only considering 1533 combinations out of possible 3^9 combinations
