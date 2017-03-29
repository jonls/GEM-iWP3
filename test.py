#!/usr/bin/env python

import logging
import unittest

from psamm.datasource import native
from psamm import fluxanalysis
from psamm.lpsolver import generic


class TestModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Load model just once
        cls.model = native.NativeModel.load_model_from_path('.')

    def test_fba_glucose_growth(self):
        """Test growth on glucose medium."""
        solver = generic.Solver()
        mm = self.model.create_metabolic_model()

        del mm.limits['EX_cpd_glc-D[e]'].lower

        fluxes = dict(fluxanalysis.flux_balance(
            mm, self.model.biomass_reaction, tfba=False, solver=solver))
        self.assertGreater(fluxes[self.model.biomass_reaction], 0.01)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    unittest.main()
