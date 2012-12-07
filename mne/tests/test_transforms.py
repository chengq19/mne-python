import os.path as op
import shutil
import tempfile

from nose.tools import assert_true
from numpy.testing import assert_array_equal

from mne.datasets import sample
from mne import read_trans, write_trans

examples_folder = op.join(op.dirname(__file__), '..', '..', 'examples')
data_path = sample.data_path(examples_folder)
fname = op.join(data_path, 'MEG', 'sample', 'sample_audvis_raw-trans.fif')


def test_io_trans():
    """Testing reading and writing of trans files
    """
    info0 = read_trans(fname)
    tempdir = tempfile.mkdtemp()
    fname1 = op.join(tempdir, 'test-trans.fif')
    write_trans(fname1, info0)
    info1 = read_trans(fname1)
    shutil.rmtree(tempdir)

    # check all properties
    assert_true(info0['from'] == info1['from'])
    assert_true(info0['to'] == info1['to'])
    assert_array_equal(info0['trans'], info1['trans'])
    for d0, d1 in zip(info0['dig'], info1['dig']):
        assert_array_equal(d0['r'], d1['r'])
        for name in ['kind', 'ident', 'coord_frame']:
            assert_true(d0[name] == d1[name])