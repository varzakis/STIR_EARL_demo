import matplotlib.pyplot as plt
import os
import shutil
import sirf.STIR as spect
import numpy as np
import numexpr as ne
ne.set_num_threads(16) # use only 16 threads
import sys
import math as m
from pathlib import Path


def display(images, slc=0, plane=0, cmap='inferno', _min=0, _max=0):
    '''
    Display images/acquisition data for a specific slice/projection and plane.

    Parameters:
    images (list of ImageData or AcquisitionData or ndarray): The input image data.
    row (int, optional): The row to be displayed (default is 0).
    cmap (str, optional): The colormap for the displayed images (default is 'inferno').
    _min (float, optional): The minimum value to be displayed (default is 0 which displays the image's own minimum).
    _max (float, optional): The maximum value to be displayed (default is 0 which displays the image's own maximum).
        
    Returns: --
    '''
    try:
        n_plots = len(images)
    except TypeError:
        n_plots = 1

    if n_plots == 1:
        im_arr = image_to_image2d(images, slc, plane)
        if (_min, _max) == (0, 0):
            _min, _max = np.amin(im_arr), np.amax(im_arr)
    else:
        im_arr = [image_to_image2d(im, slc, plane) for im in images]
        if (_min, _max) == (0, 0):
            combined_data = np.array(im_arr)
            _min, _max = np.amin(combined_data), np.amax(combined_data)
    
    fig, axes = plt.subplots(1, n_plots)
    fig.set_figheight(6)
    fig.set_figwidth(18)

    fig.suptitle(f'Display slice/projection [{slc}]', color='black', weight='bold', fontsize=20)
    if n_plots == 1:
        ax_im = axes.imshow(im_arr, cmap=cmap, vmin=_min, vmax=_max)
        fig.colorbar(ax_im)
    else:
        for i, ax in enumerate(axes.flat):
            ax_im = ax.imshow(im_arr[i], cmap=cmap, vmin=_min, vmax=_max)
            fig.colorbar(ax_im)


def image_to_image2d(img_acq, slc_or_proj:int=0, plane:int=0) -> np.array:
    '''
    Generate a 2D array from an image/acquisition data given a slice/projection and a plane. 

    Parameters:
    img_acq (ImageData or AcquisitionData or ndarray): The input image or projections.
    slc_or_proj (int, optional): The slice or projection to be displayed (default is 0).
    plane (int, optional): The plane to be displayed (0: transverse, 1: coronal, 2: sagittal, default is 0).
    
    Returns (2D ndarray): Array to be displayed.
    '''
    if type(img_acq) is np.ndarray:
        img_acq_arr = img_acq.copy()
    else:        
        img_acq_arr = img_acq.as_array()        

    image_data = False
    if img_acq_arr.ndim == 3:
        image_data = True

    if image_data:
        orientation = {
            0   :   'transverse',
            1   :   'coronal',
            2   :   'sagittal'
        }

        if plane not in orientation:
            plane = 0
            print('Display plane does not exist. Defaulting to transverse!')

        if slc_or_proj > img_acq_arr.shape[plane]:
            print(f'Total number of {orientation[plane]} slices in image is: {img_acq_arr.shape[plane]}')
            slc_or_proj = img_acq_arr.shape[plane]      

        if plane == 0:
            image2D = img_acq_arr[slc_or_proj-1,:,:]
        elif plane == 1:
            image2D = img_acq_arr[:,slc_or_proj-1,:]
        elif plane == 2:
            image2D = img_acq_arr[:,:,slc_or_proj-1]

    else:
        if plane != 0:
            print('This is acquisition data. There are no planes to display!')

        if slc_or_proj > img_acq_arr.shape[2]:
            print(f'Total projections of dataset is: {img_acq_arr.shape[2]}')
            slc_or_proj = img_acq_arr.shape[2]

        image2D = img_acq_arr[0,:,slc_or_proj-1,:]

    return image2D


def extract_header_info(hdr, tag_str:str) -> str:
    '''
    Extracts the information from header of image/acquisition data for a given tag.

    Parameters:
    hdr (ImageData or AcquisitionData or str): The ImageData, AcquisitionData or filepath of the header file.
    tag_str (str): The tag for which the value is to be extracted.
    
    Returns (str): The value of the tag.
    ''' 
    tag_value = None
    
    if type(hdr) is str:
        lines = open(hdr, 'rt')
        for line in lines:
            if line.find(tag_str) != -1:
                tag_value = line.split('= ')[1]
        lines.close()

    else:
        header = hdr.get_info()
        lines = header.split('\n')
        for line in lines:
            if line.find(tag_str) != -1:
                if len(line.split(':= ')) == 2:
                    tag_value = line.split(':= ')[1]
                elif len(line.split(': ')) == 2:
                    tag_value = line.split(': ')[1]
    
    if not tag_value:
        print(f'Tag {tag_str} not found!')
        tag_value = 'no_value'
    
    return tag_value


def replace_header_info(hdr_file:str, tag_str:str, replace_value:str):
    '''
    Changes the value for a certain tag in a header file.

    Parameters:
    hdr_file (str): The header filepath.
    tag_str (str): The tag for which the value is to be extracted.
    replace_value (str): The new value for the given tag.
    
    Returns: --
    ''' 
    # open the file and read all lines in a list
    header_file = open(hdr_file, 'rt')
    lines = header_file.readlines()
    
    # look for field_str in lines and identify the line number
    line = None
    for i in range(len(lines)):
        if lines[i].find(tag_str) != -1:
            line = i

    # replace the value if the line number is found above
    if line:
        header_file = open(hdr_file, 'wt')
        lines[line] = tag_str + ' := ' + replace_value + '\n'
        header_file.writelines(lines)
    else:
        print('Tag not found!')

    header_file.close()


def replace_header_tag(hdr_file:str, tag_str_old:str, tag_str_new:str):
    '''
    Replaces a certain tag name with another in a header file, leaving the value intact.

    Parameters:
    hdr_file (str): The header filepath.
    tag_str_old (str): The old tag.
    tag_str_new (str): The new tag.
    
    Returns: --
    '''
    old_str_value = extract_header_info(hdr_file,tag_str_old)

    # open the file and read all lines in a list
    header_file = open(hdr_file, 'rt')
    lines = header_file.readlines()
    
    # look for field_str in lines and identify the line number
    line = None
    for i in range(len(lines)):
        if lines[i].find(tag_str_old) != -1:
            line = i

    if line:
        header_file = open(hdr_file, 'wt') 
        lines[line] = tag_str_new + ' := ' + old_str_value# + '\n'
        header_file.writelines(lines)

    header_file.close()


def remove_header_info(hdr_file:str, tag_str:str):
    '''
    Removes a certain tag and value in a header file.

    Parameters:
    hdr_file (str): The header filepath.
    tag_str (str): The tag to be removed.
        
    Returns: --
    ''' 
    # open the file and read all lines in a list
    header_file = open(hdr_file, 'rt')
    lines = header_file.readlines()
    
    # look for field_str in lines and identify the line number
    line = None
    for i in range(len(lines)):
        if lines[i].find(tag_str) != -1:
            line = i

    if line:
        header_file = open(hdr_file, 'wt')  
        lines[line] = '\n'
        header_file.writelines(lines)
    else:
        print('Tag not found!')

    header_file.close()


def add_header_info(hdr_file:str, tag_name:str, tag_value:str, place_before_tag:str='!END OF INTERFILE :='):
    '''
    Adds a certain tag and its value in a header file.

    Parameters:
    hdr_file (str): The header filepath.
    tag_name (str): The tag name to be added.
    tag_value (str): The tag value to be added
        
    Returns: --
    ''' 
    # open the file and read all lines in a list
    header_file = open(hdr_file, 'rt')
    lines = header_file.readlines()
    
    # look for field_str in lines and identify the line number
    line = None
    lines_new = []
    for i in range(len(lines)):
        if lines[i].find(place_before_tag) != -1:
            lines_new.append(f'{tag_name} := {tag_value}\n')
        lines_new.append(lines[i])

    header_file = open(hdr_file, 'wt')
    header_file.writelines(lines_new)
    header_file.close()


def convert_simind_to_stir(simind_header_fp:str,contour_file=None):
    if not simind_header_fp.endswith('.h00'):
        print("This doesn't seem to be a simind header file. It should end with .h00!")
        sys.exit()

    stir_header_fp = f'{simind_header_fp[:-4]}.hs'
    shutil.copyfile(simind_header_fp,stir_header_fp)
    
    replace_header_tag(stir_header_fp,'program author',';program author')
    replace_header_tag(stir_header_fp,'program version',';program version')
    replace_header_tag(stir_header_fp,'original institution',';original institution')
    replace_header_tag(stir_header_fp,'contact person',';contact person')
    replace_header_tag(stir_header_fp,'patient name',';patient name')
    replace_header_tag(stir_header_fp,'!study ID',';!study ID')
    replace_header_tag(stir_header_fp,'data description',';data description')
    replace_header_tag(stir_header_fp,'exam type',';exam type')
    replace_header_tag(stir_header_fp,'!patient ID',';!patient ID')
    replace_header_tag(stir_header_fp,'patient position',';patient position')
    replace_header_tag(stir_header_fp,'patient orientation',';patient orientation')
    replace_header_tag(stir_header_fp,'patient orientation',';patient orientation')
    replace_header_tag(stir_header_fp,';energy window lower level','energy window lower level[1]')
    replace_header_tag(stir_header_fp,';energy window upper level','energy window upper level[1]')
    replace_header_tag(stir_header_fp,'!total number of images',';!total number of images')
    replace_header_info(stir_header_fp,'!number format', 'float')
    replace_header_tag(stir_header_fp,'number of detector heads',';number of detector heads')
    replace_header_tag(stir_header_fp,'!number of images/energy window',';!number of images/energy window')
    replace_header_tag(stir_header_fp,'!time per projection (sec)',';!time per projection (sec)')
    add_header_info(stir_header_fp,'number of time frames','1','image duration (sec)')
    replace_header_tag(stir_header_fp,'image duration (sec)','image duration (sec) [1]')
    if extract_header_info(simind_header_fp,'orbit') == 'noncircular\n':
        replace_header_info(stir_header_fp,'orbit','non-circular')
        countour_f = open(contour_file,'rt')
        radii_from_file = countour_f.readlines()
        radial_position = []
        for angle in radii_from_file:
            radial_position.append(float(angle.split('      ')[1].split('  ')[0])*10)
        radial_position_string = ','.join(map(str, radial_position))
        radial_position_string = '{' + radial_position_string + '}'
        countour_f.close()    
    add_header_info(stir_header_fp,'Radii',radial_position_string,'acquisition mode')
    replace_header_tag(stir_header_fp,'acquisition mode',';acquisition mode')
    replace_header_info(stir_header_fp,'start angle','180')


def DEW_scatter_correction(PP, SC) -> spect.AcquisitionData:
    '''
    Performs scatter correction with the Dual Energy Window method. Negative values
    are clipped after the operation.

    Parameters:
    PP (AcquisitionData or str): The acquisition data or header filepath of the photopeak window.
    SC (AcquisitionData or str): The acquisition data or header filepath of the scatter window.

    Returns (AcquisitionData): The scatter corrected projections.
    '''

    if type(PP) is str:
        acq_data_PP = spect.AcquisitionData(PP)
    else:
        acq_data_PP = PP.clone()
    acq_data_PP_arr = acq_data_PP.as_array()

    if type(SC) is str:
        acq_data_SC = spect.AcquisitionData(SC)
    else:
        acq_data_SC = SC.clone()
    acq_data_SC_arr = acq_data_SC.as_array()

    # Indicate header tags to extract, i.e. lower energy level and higher energy level
    lo_tag = 'energy window lower level[1]'
    hi_tag = 'energy window upper level[1]'
    
    # open header file, extract tags and generate window width
    # PHOTOPEAK
    lo = float(extract_header_info(PP, lo_tag))
    hi = float(extract_header_info(PP, hi_tag))
    window_width_PP = hi -lo
    print(f'PP window width: {str(round(window_width_PP,2))}')
    
    # SCATTER WINDOW
    lo = float(extract_header_info(SC, lo_tag))
    hi = float(extract_header_info(SC, hi_tag))
    window_width_SC = hi - lo
    print(f'SC window width: {str(round(window_width_SC,2))}')
    
    # estimate scatter under photopeak with DEW method    
    acq_data_scatter_DEW_arr = (acq_data_SC_arr / window_width_SC) * window_width_PP / 2
    print(f'Scatter fraction: {str(round((window_width_PP/window_width_SC) / 2, 2))}')
    
    # scatter corrected data
    acq_data_corr_arr = acq_data_PP_arr - acq_data_scatter_DEW_arr
        
    # set negative values to zero
    acq_data_corr_clipped_arr = acq_data_corr_arr.clip(min=0)
    
    # create AcquisitionData object for scatter corrected data
    acq_data_corr_clipped = acq_data_PP.clone()
    acq_data_corr_clipped.fill(acq_data_corr_clipped_arr)
    
    # return scatter corrected data
    return acq_data_corr_clipped


def TEW_scatter_correction(PP, SC1, SC2) -> spect.AcquisitionData:
    '''
    Performs scatter correction with the Triple Energy Window method. Negative values
    are clipped after the operation.

    Parameters:
    PP (AcquisitionData or str): The acquisition data or header filepath of the photopeak window.
    SC1 (AcquisitionData or str): The acquisition data or header filepath of one of the scatter windows.
    SC2 (AcquisitionData or str): The acquisition data or header filepath of the other scatter window.

    Returns (AcquisitionData): The scatter corrected projections.
    '''
    
    if type(PP) is str:
        acq_data_PP = spect.AcquisitionData(PP)
    else:
        acq_data_PP = PP.clone()
    acq_data_PP_arr = acq_data_PP.as_array()

    if type(SC1) is str:
        acq_data_SC1 = spect.AcquisitionData(SC1)
    else:
        acq_data_SC1 = SC1.clone()
    acq_data_SC1_arr = acq_data_SC1.as_array()
    
    if type(SC2) is str:
        acq_data_SC2 = spect.AcquisitionData(SC2)
    else:
        acq_data_SC2 = SC2.clone()
    acq_data_SC2_arr = acq_data_SC2.as_array()
    
    # Indicate header tags to extract, i.e. lower energy level and higher energy level
    lo_tag = 'energy window lower level[1]'
    hi_tag = 'energy window upper level[1]'
    
    # open header file, extract tags and generate window width
    # PHOTOPEAK
    lo = float(extract_header_info(PP, lo_tag))
    hi = float(extract_header_info(PP, hi_tag))
    window_width_PP = hi -lo
    print(f'PP window width: {str(round(window_width_PP,2))}')
    
    # SCATTER WINDOW 1
    lo = float(extract_header_info(SC1, lo_tag))
    hi = float(extract_header_info(SC1, hi_tag))
    window_width_SC1 = hi - lo            
    print(f'SC1 window width: {str(round(window_width_SC1,2))}')
    
    # SCATTER WINDOW 2
    lo = float(extract_header_info(SC2, lo_tag))
    hi = float(extract_header_info(SC2, hi_tag))
    window_width_SC2 = hi - lo
    print(f'SC2 window width: {str(round(window_width_SC2,2))}')
    
    # estimate scatter under photopeak with TEW method    
    acq_data_scatter_TEW_arr = ((acq_data_SC1_arr / window_width_SC1) + (acq_data_SC2_arr / window_width_SC2)) * window_width_PP / 2
    
    # scatter corrected data
    acq_data_corr_arr = acq_data_PP_arr - acq_data_scatter_TEW_arr
    
    # set negative values to zero    
    acq_data_corr_clipped_arr = acq_data_corr_arr.clip(min=0)
    
    # create AcquisitionData object for scatter corrected data
    acq_data_corr_clipped = acq_data_PP.clone()
    acq_data_corr_clipped.fill(acq_data_corr_clipped_arr)
    
    # return scatter corrected data
    return acq_data_corr_clipped