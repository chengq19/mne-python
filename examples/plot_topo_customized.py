"""
========================================
Plot custom topographies for MEG sensors
========================================

This example exposes the `iter_topography` function that makes it
very easy to generate custom sensor topography plots.
Here we will plot the power spectrum of each channel on a topographic
layout.

"""

# Author: Denis A. Engemann <denis.engemann@gmail.com>
#
# License: BSD (3-clause)

print(__doc__)

import numpy as np
import mne

from mne.viz import iter_topography
from mne import io
from mne.time_frequency import compute_raw_psd

import matplotlib.pyplot as plt

from mne.datasets import sample
data_path = sample.data_path()
raw_fname = data_path + '/MEG/sample/sample_audvis_filt-0-40_raw.fif'

raw = io.Raw(raw_fname, preload=True)
raw.filter(1, 20)

picks = mne.pick_types(raw.info, meg=True, exclude=[])
tmin, tmax = 0, 120  # use the first 120s of data
fmin, fmax = 2, 20  # look at frequencies between 2 and 20Hz
n_fft = 2048  # the FFT size (n_fft). Ideally a power of 2
psds, freqs = compute_raw_psd(raw, picks=picks, tmin=tmin, tmax=tmax,
                              fmin=fmin, fmax=fmax)
psds = 20 * np.log10(psds)  # scale to dB


def my_callback(ax, ch_idx):
    """
    This block of code is executed once you click on one of the channel axes
    in the plot. To work with the viz internals, this function should only take
    two parameters, the axis and the channel or data index.
    """
    ax.plot(freqs, psds[ch_idx], color='red')
    ax.set_xlabel = 'Frequency (Hz)'
    ax.set_ylabel = 'Power (dB)'

for ax, idx in iter_topography(raw.info,
                               fig_facecolor='white',
                               axis_facecolor='white',
                               axis_spinecolor='white',
                               on_pick=my_callback):
    ax.plot(psds[idx], color='red')

plt.gcf().suptitle('Power spectral densities')
plt.show()
