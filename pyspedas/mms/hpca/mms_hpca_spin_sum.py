import numpy as np
from pytplot import get_data, store_data, options
from pyspedas import tnames

def mms_hpca_spin_sum(probe = '1', datatypes=None, species=['hplus', 'oplus', 'oplusplus', 'heplus', 'heplusplus'], fov=['0', '360'], avg=False):
    """
    This function will sum (or average, when the avg keyword is set to True) the HPCA data over each spin
    Parameters:
        fov : list of str
            field of view, in angles, from 0-360
        probe : str
            probe #, e.g., '4' for MMS4
        suffix: str
            suffix of the loaded data

    Returns:
        List of tplot variables created.
    """
    if datatypes is None:
        datatypes = ['*_count_rate', '*_RF_corrected', '*_bkgd_corrected', '*_norm_counts', '*_flux']
    else:
        if isinstance(datatypes, list):
            datatypes = ['*_'+dt for dt in datatypes]
        else:
            datatypes = ['*_'+datatypes]

    az_times, start_az = get_data('mms'+probe+'_hpca_start_azimuth')

    spin_starts = np.argwhere(start_az == 0)
    output_vars = []

    for datatype in datatypes:
        vars_to_sum = tnames(datatype+'_elev_'+fov[0]+'-'+fov[1])
        for var in vars_to_sum:
            data = get_data(var, xarray=True)
            out_data = []
            for i, spin_start in enumerate(spin_starts[:-1]):
                if avg:
                    out_data.append(data[spin_start[0]:spin_starts[i+1][0]].mean(dim='time'))
                else:
                    out_data.append(data[spin_start[0]:spin_starts[i+1][0]].sum(dim='time'))
            out_times = [t[0] for t in az_times[spin_starts[:-1]]]
            store_data(var+'_spin', data={'x': out_times, 'y': out_data, 'v': data.coords['spec_bins'].values})
            options(var+'_spin', 'spec', True)
            options(var+'_spin', 'ylog', True)
            options(var+'_spin', 'zlog', True)
            options(var+'_spin', 'Colormap', 'jet')
            output_vars.append(var+'_spin')
    return output_vars