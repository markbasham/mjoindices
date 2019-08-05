# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 13:01:37 2019

@author: ch
"""

import warnings
from pathlib import Path

import numpy as np

import mjoindex_omi.olr_handling as olr
import mjoindex_omi.omi_calculator as omi
import mjoindex_omi.plotting as plotting


def compare_Recalc_OMI_PCs_OriginalOLROriginalEOFs():
    """ Calulates and plots OMI PCs, which are compareable to the original PCs.

    The calculations is based based on the original EOFs and the original OLR
    dataset. Both have to be downloaded and stored locally before the example
    is executeable

    Furthermore, the original OMI PC file is needed to be able to procude the
    comparison plot.

    See tests/testdata/README for download links and local storage directories.

    """

    olr_data_filename = Path(__file__).parent / "tests" / "testdata" / "olr.day.mean.nc"
    originalOMIDataDirname = Path(__file__).parent / "tests" / "testdata" / "OriginalOMI"
    origOMIPCsFilename = originalOMIDataDirname / "omi.1x.txt"

    if not olr_data_filename.is_file():
        raise Exception("OLR data file not available. Expected file: %s" % olr_data_filename)

    if not originalOMIDataDirname.is_dir():
        raise Exception("Path to original OMI EOFs is missing. Expected path: %s" % originalOMIDataDirname)

    if not origOMIPCsFilename.is_file():
        warnings.warn(
            "File with the original OMI PCs are missing. Generation of the comparison plot will fail. Expected file: %s" % origOMIPCsFilename)

    resultfile = Path(__file__).parent / "example_data" / "RecalcPCsOrigOLROrigEOF.txt"
    
    resultfigfile = Path(__file__).parent / "example_data" / "RecalcPCsOrigOLROrigEOF"

    olrData = olr.load_noaa_interpolated_olr(olr_data_filename)
    target = omi.calculatePCsFromOLRWithOriginalConditions(
        olrData,
        originalOMIDataDirname,
        useQuickTemporalFilter=True)
    target.save_pcs_to_txt_file(resultfile)

    fig = plotting.plotComparisonOrigRecalcPCs(resultfile, origOMIPCsFilename, np.datetime64("2011-06-01"),
                                               np.datetime64("2011-12-31"))
    fig.show()
    fig.savefig(resultfigfile.with_suffix(".png"), bbox_inches='tight')
    fig.savefig(resultfigfile.with_suffix(".pdf"), bbox_inches='tight')


if __name__ == '__main__':
    compare_Recalc_OMI_PCs_OriginalOLROriginalEOFs()
