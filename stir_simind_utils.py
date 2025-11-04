import matplotlib.pyplot as plt
import os
import shutil
from sirf_simind_connection.backends import AcquisitionDataInterface
import numpy as np
import sys
import math as m
from pathlib import Path
from typing import Optional


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


def DEW_scatter_correction(PP: AcquisitionDataInterface, SC: AcquisitionDataInterface,
                           PP_bounds=None, SC_bounds=None) -> AcquisitionDataInterface:
    '''
    Performs scatter correction with the Dual Energy Window method. Negative values
    are clipped after the operation.

    Parameters:
    PP (AcquisitionDataInterface): The acquisition data of the photopeak window.
    SC (AcquisitionDataInterface): The acquisition data of the scatter window.
    PP_bounds (tuple, optional): (lower, upper) energy bounds for PP window in keV.
                                 If None, will extract from PP acquisition data.
    SC_bounds (tuple, optional): (lower, upper) energy bounds for SC window in keV.
                                 If None, will extract from SC acquisition data.

    Returns (AcquisitionDataInterface): The scatter corrected projections.
    '''

    acq_data_PP = PP.clone()
    acq_data_SC = SC.clone()

    # Get energy window bounds - either from parameters or from acquisition data
    if PP_bounds is None:
        lo_PP, hi_PP = acq_data_PP.get_energy_window_bounds()
    else:
        lo_PP, hi_PP = PP_bounds
    window_width_PP = hi_PP - lo_PP
    print(f'PP window width: {str(round(window_width_PP, 2))}')

    if SC_bounds is None:
        lo_SC, hi_SC = acq_data_SC.get_energy_window_bounds()
    else:
        lo_SC, hi_SC = SC_bounds
    window_width_SC = hi_SC - lo_SC
    print(f'SC window width: {str(round(window_width_SC, 2))}')

    # Calculate scatter fraction
    scatter_fraction = (window_width_PP / window_width_SC) / 2
    print(f'Scatter fraction: {str(round(scatter_fraction, 2))}')

    # Estimate scatter under photopeak with DEW method using AcquisitionData operations
    # Formula: scatter = (SC / window_width_SC) * window_width_PP / 2
    acq_data_scatter = acq_data_SC * scatter_fraction

    # Scatter corrected data using AcquisitionData subtraction
    acq_data_corr = acq_data_PP - acq_data_scatter

    # Set negative values to zero using numpy array operations
    acq_data_corr_arr = acq_data_corr.as_array()
    acq_data_corr_arr[acq_data_corr_arr < 0] = 0
    acq_data_corr.fill(acq_data_corr_arr)

    # return scatter corrected data
    return acq_data_corr


def TEW_scatter_correction(PP: AcquisitionDataInterface, SC1: AcquisitionDataInterface,
                           SC2: AcquisitionDataInterface, PP_bounds=None, SC1_bounds=None,
                           SC2_bounds=None) -> AcquisitionDataInterface:
    '''
    Performs scatter correction with the Triple Energy Window method. Negative values
    are clipped after the operation.

    Parameters:
    PP (AcquisitionDataInterface): The acquisition data of the photopeak window.
    SC1 (AcquisitionDataInterface): The acquisition data of one of the scatter windows.
    SC2 (AcquisitionDataInterface): The acquisition data of the other scatter window.
    PP_bounds (tuple, optional): (lower, upper) energy bounds for PP window in keV.
                                 If None, will extract from PP acquisition data.
    SC1_bounds (tuple, optional): (lower, upper) energy bounds for SC1 window in keV.
                                  If None, will extract from SC1 acquisition data.
    SC2_bounds (tuple, optional): (lower, upper) energy bounds for SC2 window in keV.
                                  If None, will extract from SC2 acquisition data.

    Returns (AcquisitionDataInterface): The scatter corrected projections.
    '''

    acq_data_PP = PP.clone()
    acq_data_SC1 = SC1.clone()
    acq_data_SC2 = SC2.clone()

    # Get energy window bounds - either from parameters or from acquisition data
    if PP_bounds is None:
        lo_PP, hi_PP = acq_data_PP.get_energy_window_bounds()
    else:
        lo_PP, hi_PP = PP_bounds
    window_width_PP = hi_PP - lo_PP
    print(f'PP window width: {str(round(window_width_PP, 2))}')

    if SC1_bounds is None:
        lo_SC1, hi_SC1 = acq_data_SC1.get_energy_window_bounds()
    else:
        lo_SC1, hi_SC1 = SC1_bounds
    window_width_SC1 = hi_SC1 - lo_SC1
    print(f'SC1 window width: {str(round(window_width_SC1, 2))}')

    if SC2_bounds is None:
        lo_SC2, hi_SC2 = acq_data_SC2.get_energy_window_bounds()
    else:
        lo_SC2, hi_SC2 = SC2_bounds
    window_width_SC2 = hi_SC2 - lo_SC2
    print(f'SC2 window width: {str(round(window_width_SC2, 2))}')

    # Estimate scatter under photopeak with TEW method using AcquisitionData operations
    # Formula: scatter = ((SC1 / width_SC1) + (SC2 / width_SC2)) * width_PP / 2
    scatter_fraction_1 = window_width_PP / (2 * window_width_SC1)
    scatter_fraction_2 = window_width_PP / (2 * window_width_SC2)

    acq_data_scatter = acq_data_SC1 * scatter_fraction_1 + acq_data_SC2 * scatter_fraction_2

    # Scatter corrected data using AcquisitionData subtraction
    acq_data_corr = acq_data_PP - acq_data_scatter

    # Set negative values to zero using numpy array operations
    acq_data_corr_arr = acq_data_corr.as_array()
    acq_data_corr_arr[acq_data_corr_arr < 0] = 0
    acq_data_corr.fill(acq_data_corr_arr)

    # return scatter corrected data
    return acq_data_corr


def add_poisson_noise(acq_data: AcquisitionDataInterface,
                      rng: Optional[np.random.Generator] = None
                      ) -> AcquisitionDataInterface:
    '''
    Add Poisson noise to acquisition data and return a new instance with the noisy counts.

    Parameters:
    acq_data (AcquisitionDataInterface): The acquisition data to be perturbed.
    rng (np.random.Generator, optional): Optional random generator for reproducibility.

    Returns (AcquisitionDataInterface): Noisy acquisition data.
    '''
    if rng is None:
        rng = np.random.default_rng()

    counts = np.clip(acq_data.as_array(), a_min=0, a_max=None)

    noisy_counts = rng.poisson(counts)

    noisy_acq = acq_data.clone()
    noisy_acq.fill(noisy_counts.astype(counts.dtype, copy=False))
    return noisy_acq

def update_par_file(par_file_path: str, output_par_path: str, updates: dict) -> str:
    '''
    Update parameters in a STIR par file and save to a new location.
    Only updates lines that exactly match the parameter name (before :=).

    Parameters:
    par_file_path (str): Path to the original par file.
    output_par_path (str): Path where the updated par file will be saved.
    updates (dict): Dictionary of parameter names and their new values.
                    Example: {'input file': 'data.hs', 'output filename prefix': 'recon_result'}

    Returns (str): Path to the updated par file.
    '''
    # Read the original par file
    with open(par_file_path, 'r') as f:
        lines = f.readlines()

    # Update parameters - be more precise with matching
    updated_lines = []
    for line in lines:
        line_updated = False

        # Only process lines with :=
        if ':=' in line:
            # Extract the parameter name (text before :=)
            param_name_in_line = line.split(':=')[0].strip()

            # Check if this parameter should be updated
            for param_name, param_value in updates.items():
                if param_name_in_line.lower() == param_name.lower():
                    # Extract indentation
                    indent = len(line) - len(line.lstrip())
                    updated_lines.append(' ' * indent + f'{param_name} := {param_value}\n')
                    line_updated = True
                    break

        if not line_updated:
            updated_lines.append(line)

    # Write the updated par file
    with open(output_par_path, 'w') as f:
        f.writelines(updated_lines)

    return output_par_path


def reconstruct_with_osem(input_file: str, output_prefix: str, par_file_template: str,
                          initial_image_template, attenuation_image, num_subsets: int = 4,
                          num_subiterations: int = 24, temp_dir: str = './temp_recon'):
    '''
    Perform OSEM reconstruction using STIR with a modified par file.

    Parameters:
    input_file (str): Path to the input acquisition data (.hs file).
    output_prefix (str): Prefix for output files.
    par_file_template (str): Path to the template par file.
    initial_image_template: STIR image object to use as template for initial image.
    attenuation_image: STIR image object containing attenuation map.
    num_subsets (int): Number of subsets for OSEM (default: 4).
    num_subiterations (int): Number of subiterations (default: 24).
    temp_dir (str): Directory for temporary files (default: './temp_recon').

    Returns: The reconstructed image (stir.FloatVoxelsOnCartesianGrid).
    '''
    import stir
    from pathlib import Path

    # Create temp directory if it doesn't exist
    Path(temp_dir).mkdir(parents=True, exist_ok=True)

    # Convert all paths to absolute paths
    temp_dir_abs = os.path.abspath(temp_dir)
    input_file_abs = os.path.abspath(input_file)
    par_file_template_abs = os.path.abspath(par_file_template)

    # Create and save required images
    # 1. Initial estimate
    target = initial_image_template.clone()
    target.fill(1.0)
    init_file = os.path.join(temp_dir_abs, f'{output_prefix}_init.hv')
    target.write_to_file(init_file)

    # 2. Attenuation map
    atten_file = os.path.join(temp_dir_abs, f'{output_prefix}_atten.hv')
    attenuation_image.write_to_file(atten_file)

    # 3. Mask (create from attenuation map - non-zero values)
    mask = attenuation_image.clone()
    mask_arr = mask.as_array()
    mask_arr[mask_arr > 0] = 1.0
    mask.fill(mask_arr)
    mask_file = os.path.join(temp_dir_abs, f'{output_prefix}_mask.hv')
    mask.write_to_file(mask_file)

    # Create modified par file with all necessary paths
    temp_par_file = os.path.join(temp_dir_abs, f'{output_prefix}_recon.par')
    updates = {
        'input file': input_file_abs,
        'output filename prefix': os.path.join(temp_dir_abs, output_prefix),
        'initial estimate': init_file,
        'attenuation map': atten_file,
        'mask file': mask_file,
        'number of subsets': num_subsets,
        'number of subiterations': num_subiterations,
    }

    update_par_file(par_file_template_abs, temp_par_file, updates)

    # Initialize reconstruction object
    recon = stir.OSMAPOSLReconstruction3DFloat(temp_par_file)

    # Set up reconstruction
    s = recon.set_up(target)
    if not s.succeeded():
        raise RuntimeError(f'Error setting up reconstruction for {output_prefix}')

    # Run reconstruction
    print(f'Running reconstruction for {output_prefix}...')
    print(f'  Input file: {input_file}')
    print(f'  Subsets: {num_subsets}, Subiterations: {num_subiterations}')

    recon.set_start_subiteration_num(1)
    recon.set_num_subiterations(num_subiterations)
    s = recon.reconstruct(target)

    if not s.succeeded():
        raise RuntimeError(f'Reconstruction failed for {output_prefix}')

    # Save the reconstructed image
    output_filename = os.path.join(temp_dir, f'{output_prefix}.hv')
    target.write_to_file(output_filename)
    print(f'Reconstruction complete. Saved to: {output_filename}')

    return target


def compare_reconstructions(recon_dict: dict, slice_idx: int = None, cmap: str = 'hot',
                           vmin: float = None, vmax: float = None):
    '''
    Compare multiple reconstructed images side by side.

    Parameters:
    recon_dict (dict): Dictionary of {name: stir.FloatVoxelsOnCartesianGrid} pairs.
    slice_idx (int, optional): Slice index to display. If None, uses middle slice.
    cmap (str): Colormap for display (default: 'hot').
    vmin (float, optional): Minimum value for color scale.
    vmax (float, optional): Maximum value for color scale.

    Returns: matplotlib figure and axes objects.
    '''
    n_images = len(recon_dict)
    fig, axes = plt.subplots(1, n_images, figsize=(6*n_images, 5))

    if n_images == 1:
        axes = [axes]

    # Get all arrays for consistent scaling
    arrays = []
    for name, img in recon_dict.items():
        if hasattr(img, 'as_array'):
            arr = img.as_array()
        else:
            arr = img
        arrays.append(arr)

    # Determine slice index if not provided
    if slice_idx is None:
        slice_idx = arrays[0].shape[0] // 2

    # Determine color scale if not provided
    if vmin is None or vmax is None:
        all_data = np.concatenate([arr[slice_idx, :, :].flatten() for arr in arrays])
        if vmin is None:
            vmin = np.min(all_data)
        if vmax is None:
            vmax = np.max(all_data)

    # Plot each image
    for idx, (name, img) in enumerate(recon_dict.items()):
        arr = arrays[idx]
        im = axes[idx].imshow(arr[slice_idx, :, :], cmap=cmap, vmin=vmin, vmax=vmax)
        axes[idx].set_title(name, fontsize=14, fontweight='bold')
        axes[idx].axis('off')
        plt.colorbar(im, ax=axes[idx], fraction=0.046, pad=0.04)

    fig.suptitle(f'Reconstruction Comparison (Slice {slice_idx})', fontsize=16, fontweight='bold')
    plt.tight_layout()

    return fig, axes
