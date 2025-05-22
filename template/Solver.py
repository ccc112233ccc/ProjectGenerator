# import matlab.engine
from scipy.constants import mu_0, epsilon_0, c
import pandas as pd
from enum import Enum
import numpy as np
from UI.tools import Distance, Frequency, Conductivity, Permeability, Float, Int
class ModelType(Enum):
    PN = 1
    LDMOS = 2
    JFET = 3

class AlgorithmType(Enum):
    FVM = 1
    FDTD = 2
    FEM = 3




class Solver:
    @staticmethod
    def get_solver(mode=1):
        if mode == 1:
            return Solver.PN
        else:
            raise ValueError(f"Unknown mode: {mode}")
    @staticmethod
    def PN(
        model_type: ModelType = ModelType.PN,
        algorithm_type: AlgorithmType = AlgorithmType.FVM,
        max_iteration: Int = 10,
        eps_ref: Float = 1e-8,
        err_ref_poisson: Float = 0.025852,
        err_ref_electron: Float = 1e11,
        err_ref_hole: Float = 1e11,
        scal_dop: Float = 1e22,
        rhs_ref_poisson: Float = 1e-16,
        rhs_ref_electron: Float = 1e-12,
        rhs_ref_hole: Float = 1e-12,
        exit_on_failure: Int = 1,
        rhs_factor: Float = 1e10,
        negative_value_err: Int = 1,
        area_factor: Float = 1,
    ):
        """
        This function is a placeholder for the actual solver implementation.
        It currently returns a DataFrame with the input parameters.
        """
        # 调用的具体求解器






