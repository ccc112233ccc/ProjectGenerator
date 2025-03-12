import matlab.engine
import numpy as np
import pandas as pd
import fire


class CableSolver:

    @staticmethod
    def get_solver(mode=1):
        if mode == 1:
            return CableSolver.twinax_cable_1
        elif mode == 2:
            return CableSolver.star_quad_cable
        elif mode == 3:
            return CableSolver.TWP_far_field
        elif mode == 4:
            return CableSolver.TBTWP_far_field
        else:
            raise ValueError(f"Unknown mode: {mode}")

    @staticmethod
    def twinax_cable_1(rw: float = 0.415e-3/2, D: float = 1.42e-3, rsh: float = 1.42e-3, epsir: float = 2, TanLoss: float = 5e-4, tsh: float = 9e-6, Lz: float = 0.2, segmaAL: float = 38160000, segmaCu: float = 58130000, slot_d: float = 0.07e-3, fmin: float = 1e9, fmax: float = 10e9, Np: int = 500):
        eng = matlab.engine.start_matlab()
        s_params2, sscd21, sscd11, sscc21, sscc11, ssdd21, ssdd11, f = eng.twinax_cable_1(
            rw, D, rsh, epsir, TanLoss, tsh, Lz, segmaAL, segmaCu, slot_d, fmin, fmax, Np, nargout=8
        )
        eng.quit()
        df = pd.DataFrame(
            {
                "f": np.array(f).squeeze(),
                "sscd21": np.array(sscd21).squeeze(),
                "sscd11": np.array(sscd11).squeeze(),
                "sscc21": np.array(sscc21).squeeze(),
                "sscc11": np.array(sscc11).squeeze(),
                "ssdd21": np.array(ssdd21).squeeze(),
                "ssdd11": np.array(ssdd11).squeeze(),
                "s11": np.array(s_params2).squeeze()[1, 1],
                "s21": np.array(s_params2).squeeze()[2, 1],
                "s12": np.array(s_params2).squeeze()[1, 2],
                "s22": np.array(s_params2).squeeze()[2, 2],
            }
        )
        df.to_csv(f"results.csv", index=False)

    @staticmethod
    def star_quad_cable(s: float = 2.5e-3, h: float = 1e-2, rw: float = 0.25e-3, p: float = 5e-2, Lz: float = 1, fmin: float = 1e9, fmax: float = 10e9, Np: int = 500):
        eng = matlab.engine.start_matlab()
        ICM, IDM2, f = eng.star_quad_cable(
            s, h, rw, p, Lz, fmin, fmax, Np, nargout=3)
        eng.quit()

        df = pd.DataFrame(
            {
                "f": np.array(f).squeeze(),
                "ICM": np.array(ICM).squeeze(),
                "IDM2": np.array(IDM2).squeeze(),
            }
        )
        df.to_csv(f"results.csv", index=False)

    @staticmethod
    def TWP_far_field(s: float = 0.25e-2, h: float = 1e-2, rw: float = 1.46e-9, p: float = 5e-2, Lz: float = 1, fmin: float = 1e9, fmax: float = 10e9, Np: int = 500):
        eng = matlab.engine.start_matlab()
        CMC, DMC, f = eng.TWP_far_field(
            s, h, rw, p, Lz, fmin, fmax, Np, nargout=3)
        eng.quit()

        df = pd.DataFrame(
            {
                "f": np.array(f).squeeze(),
                "CMC": np.array(CMC).squeeze(),
                "DMC": np.array(DMC).squeeze(),
            }
        )
        df.to_csv(f"results.csv", index=False)

    @staticmethod
    def TBTWP_far_field(Lz: float = 1, acc: float = 0.0001, pb: float = 25e-3, p: float = 5e-3, s: float = 0.7e-3, sb: float = 1.5e-3, rw: float = 0.15e-3, h: float = 5e-3, fmin: float = 1e9, fmax: float = 10e9, Np: int = 500):
        eng = matlab.engine.start_matlab()
        CMC, DMC, f = eng.TBTWP_far_field(
            Lz, acc, pb, p, s, sb, rw, h, fmin, fmax, Np, nargout=3)
        eng.quit()

        df = pd.DataFrame(
            {
                "f": np.array(f).squeeze(),
                "CMC": np.array(CMC).squeeze(),
                "DMC": np.array(DMC).squeeze(),
            }
        )
        df.to_csv(f"results.csv", index=False)
