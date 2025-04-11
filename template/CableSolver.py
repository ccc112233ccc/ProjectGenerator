# import matlab.engine
from scipy.constants import mu_0, epsilon_0, c
import pandas as pd
from enum import Enum
import numpy as np
from UI.tools import Distance, Frequency, Conductivity, Permeability, Float, Int

class GroundType(Enum):
    Concrete = 1
    Asphalt = 2
    DrySoil = 3
    WetSoil = 4
    FreshWater = 5
    SaltWater = 6
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
        elif mode == 5:
            return CableSolver.triphase_cable
        elif mode == 6:
            return CableSolver.JEPJ85_NSC
        elif mode == 7:
            return CableSolver.JYJPJ80_SC1
        elif mode == 8:
            return CableSolver.JYJPJ85_SC1
        elif mode == 9:
            return CableSolver.JHRPJ_SC
        elif mode == 10:
            return CableSolver.JHYJPQ85_SC
        elif mode == 11:
            return CableSolver.JHYJ85_NSC
        elif mode == 12:
            return CableSolver.JHYJP85_NSC
        elif mode == 13:
            return CableSolver.JHQYJPA86_SC
        elif mode == 14:
            return CableSolver.JKEPJP85_SC
        elif mode == 15:
            return CableSolver.JKEPJPM85_SC
        elif mode == 16:
            return CableSolver.JHEPJPM85_SC
        elif mode == 17:
            return CableSolver.JKMEHP8H_45
        else:
            raise ValueError(f"Unknown mode: {mode}")

    @staticmethod
    def twinax_cable_1(rw: Distance = 0.415e-3/2, D: Distance = 1.42e-3, rsh: Distance = 1.42e-3, epsir: float = 2, TanLoss: float = 5e-4, tsh: Distance = 9e-6, Lz: Distance = 0.2, segmaAL: Conductivity = 38160000, segmaCu: Conductivity = 58130000, slot_d: Distance = 0.07e-3, fmin: Frequency = 1e6, fmax: Frequency = 1e9, Np: int = 500):
        from codes.twinax_cable_1 import twinax_cable_1
        s_params2, sscd21, sscd11, sscc21, sscc11, ssdd21, ssdd11, f = twinax_cable_1(rw, D, rsh, epsir, TanLoss, tsh, Lz, segmaAL, segmaCu, slot_d, fmin, fmax, Np)
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
    def star_quad_cable(s: Distance = 2.5e-3, h: Distance = 1e-2, rw: Distance = 0.25e-3, p: Distance = 5e-2, Lz: Distance = 1, fmin: Frequency = 1e6, fmax: Frequency = 1e9, Np: int = 500):
        from codes.star_quad_cable import star_quad_cable
        ICM, IDM2, f = star_quad_cable(
            s, h, rw, p, Lz, fmin, fmax, Np)

        df = pd.DataFrame(
            {
                "f": np.array(f).squeeze(),
                "ICM": np.array(ICM).squeeze(),
                "IDM2": np.array(IDM2).squeeze(),
            }
        )
        df.to_csv(f"results.csv", index=False)

    @staticmethod
    def TWP_far_field(s: Distance = 0.25e-2, h: Distance = 1e-2, rw: Distance = 1.46e-9, p: Distance = 5e-2, Lz: Distance = 1, fmin: Frequency = 1e6, fmax: Frequency = 1e9, Np: int = 500):
        from codes.TWP_far_field import TWP_far_field
        CMC, DMC, f = TWP_far_field(
            s, h, rw, p, Lz, fmin, fmax, Np, nargout=3)
        df = pd.DataFrame(
            {
                "f": np.array(f).squeeze(),
                "CMC": np.array(CMC).squeeze(),
                "DMC": np.array(DMC).squeeze(),
            }
        )
        df.to_csv(f"results.csv", index=False)

    @staticmethod
    def TBTWP_far_field(Lz: Distance = 1, acc: Float = 0.0001, pb: Distance = 25e-3, p: Distance = 5e-3, s: Distance = 0.7e-3, sb: Distance = 1.5e-3, rw: Distance = 0.15e-3, h: Distance = 5e-3, fmin: Frequency = 1e6, fmax: Frequency = 1e9, Np: int = 500):
        from codes.TBTWP_far_field import TBTWP_far_field
        CMC, DMC, f = TBTWP_far_field(Lz, acc, pb, p, s, sb, rw, h, fmin, fmax, Np)
        df = pd.DataFrame(
            {
                "f": np.array(f).squeeze(),
                "CMC": np.array(CMC).squeeze(),
                "DMC": np.array(DMC).squeeze(),
            }
        )
        df.to_csv(f"results.csv", index=False)

    @staticmethod
    def triphase_cable(r_cond :Distance = 6.5e-3, rsh :Distance = 0.0309, Rsh :Distance = 0.0329, length :Distance = 2, cable1_x :Distance = 0.01443376, cable1_y :Distance = 0, cable2_x :Distance = -0.00721688, cable2_y :Distance = 0.0125, cable3_x :Distance = -0.00721688, cable3_y :Distance = -0.0125, sigma_cond :Conductivity = 5.813e7, sigma_shield :Conductivity = 3.816e7, mu :Permeability = mu_0, epsr :Float = 1, tan_delta :Float = 0, freq_min :Frequency = 1, freq_max :Frequency = 100e6, num_points :Int = 2001):
        from codes.triphase_cable import calc_triphase_sparams_v2
        # 计算三相电缆的 S 参数
        s_params, S_mixed, freq_out = calc_triphase_sparams_v2(
            r_cond, rsh, Rsh, length, cable1_x, cable1_y, cable2_x, cable2_y, cable3_x, cable3_y,
            sigma_cond, sigma_shield, mu, epsr, tan_delta, freq_min, freq_max, num_points
        )
        # 将结果转换为 DataFrame
        df = pd.DataFrame(
            {
                "f": freq_out,
                "S11": s_params[0, 0, :],
                "S12": s_params[0, 1, :],
                "S21": s_params[1, 0, :],
                "S22": s_params[1, 1, :],
            }
        )
        # 保存结果到 CSV 文件
        df.to_csv(f"results.csv", index=False)

    @staticmethod
    def JEPJ85_NSC(Conductor_Radius, Mica_Tape_Radius, Insulation_Radius, Wrapping_Tape_Radius,
                   Inner_Sheath_Radius, Armor_Radius, Outer_Sheath_Radius, Ground_Type: GroundType = GroundType.Concrete):
        """
        计算 JEPJ85 NSC 电缆的几何参数
        :param Conductor_Radius: 导体半径
        :param Mica_Tape_Radius: 云母带半径
        :param Insulation_Radius: 绝缘层半径
        :param Wrapping_Tape_Radius: 绕包带半径
        :param Inner_Sheath_Radius: 内护套半径
        :param Armor_Radius: 铠装半径
        :param Outer_Sheath_Radius: 外护套半径
        """
        print(f"Groud Type: {Ground_Type}")
        pass  # 这里暂时不做任何计算，后续可以添加逻辑

    def JYJPJ80_SC1(Conductor_Radius, Insulation_Radius, Wrapping_Tape_Radius, Sheath_Radius, Armor_Radius):
        """
        计算 JYJPJ80_SC1 电缆的几何参数

        :param Conductor_Radius: 导体半径
        :param Insulation_Radius: 绝缘层半径
        :param Wrapping_Tape_Radius: 绕包带半径
        :param Sheath_Radius: 内护套半径
        :param Armor_Radius: 铠装半径
        """
        pass  # 这里暂时不做任何计算，后续可以添加逻辑

    def JYJPJ85_SC1(Conductor_Radius, Insulation_Radius, Wrapping_Tape_Radius,
                    Inner_Sheath_Radius, Armor_Radius, Outer_Sheath_Radius):
        """
        计算 JYJPJ85_SC1 电缆的几何参数

        :param Conductor_Radius: 导体半径
        :param Insulation_Radius: 绝缘层半径
        :param Wrapping_Tape_Radius: 绕包带半径
        :param Inner_Sheath_Radius: 内护套半径
        :param Armor_Radius: 铠装半径
        :param Outer_Sheath_Radius: 外护套半径
        """
        pass  # 这里暂时不做任何计算，后续可以添加逻辑

    def JYJPJ85_SC(Conductor_Radius, Insulation_Radius, Wrapping_Tape_Radius, Sheath_Radius):
        """
        计算 JYJPJ85_SC7 七芯电缆的几何参数

        :param Conductor_Radius: 单根导体的半径
        :param Insulation_Radius: 绝缘层半径（包括导体）
        :param Wrapping_Tape_Radius: 绕包带半径
        :param Sheath_Radius: 外护套半径
        """
        pass  # 这里暂时不做任何计算，后续可以添加逻辑

    def JHYJPQ85_SC(Conductor_Radius, Insulation_Radius, Insulation_Outer_Radius,
                    Wrapping_Tape_Radius, Armor_Radius, Outer_Sheath_Radius):
        """
        计算 JHYJPQ85_SC 七芯电缆的几何参数

        :param Conductor_Radius: 单根导体的半径
        :param Insulation_Radius: 绝缘层内半径（即导体外边界）
        :param Insulation_Outer_Radius: 绝缘层外半径
        :param Wrapping_Tape_Radius: 绕包带外半径
        :param Armor_Radius: 铠装层外半径
        :param Outer_Sheath_Radius: 外护套层外半径
        """
        pass  # 这里暂时不做任何计算，后续可以添加逻辑

    def JHYJ85_NSC(Conductor_Radius, Mica_Tape_Radius, Insulation_Radius,
                   Wrapping_Tape_Radius, Armor_Radius, Outer_Sheath_Radius):
        """
        计算 JHYJ85_NSC 电缆的几何参数

        :param Conductor_Radius: 导体半径
        :param Mica_Tape_Radius: 云母带半径
        :param Insulation_Radius: 绝缘层半径
        :param Wrapping_Tape_Radius: 绕包带半径
        :param Armor_Radius: 铠装层半径
        :param Outer_Sheath_Radius: 外护套层半径
        """
        pass  # 这里暂时不做任何计算，后续可以添加逻辑

    def JHYJP85_NSC(Conductor_Radius, Mica_Tape_Radius, Insulation_Radius,
                    Individual_Insulation_Radius, Wrapping_Tape_Radius,
                    Armor_Radius, Outer_Sheath_Radius):
        """
        计算 JHYJP85_NSC 电缆的几何参数

        :param Conductor_Radius: 导体半径
        :param Mica_Tape_Radius: 云母带半径
        :param Insulation_Radius: 绝缘层总半径
        :param Individual_Insulation_Radius: 单芯绝缘层半径
        :param Wrapping_Tape_Radius: 绕包带外半径
        :param Armor_Radius: 铠装层外半径
        :param Outer_Sheath_Radius: 外护套层外半径
        """
        pass  # 这里暂时不做任何计算，后续可以添加逻辑

    def JHQYJPA86_SC(Conductor_Radius, Insulation_Radius,
                     Aluminum_Plastic_Composite_Tape_Radius, Inner_Sheath_Radius,
                     Copper_Leakage_Wire_Radius, Wrapping_Tape_Radius,
                     Armor_Radius, Outer_Sheath_Radius):
        """
        计算 JHQYJPA86_SC 电缆的几何参数

        :param Conductor_Radius: 导体半径
        :param Insulation_Radius: 绝缘层半径
        :param Aluminum_Plastic_Composite_Tape_Radius: 铝塑复合带半径
        :param Inner_Sheath_Radius: 内护套层半径
        :param Copper_Leakage_Wire_Radius: 铜泄露线半径
        :param Wrapping_Tape_Radius: 绕包带外半径
        :param Armor_Radius: 铠装层外半径
        :param Outer_Sheath_Radius: 外护套层外半径
        """
        pass  # 这里暂时不做任何计算，后续可以添加逻辑

    def JKEPJP85_SC(Conductor_Radius, EPR_Tape_Radius, Insulation_Radius,
                    Wrapping_Tape_Radius, Inner_Sheath_Radius,
                    Armor_Radius, Outer_Sheath_Radius):
        """
        计算 JKEPJP85_SC 电缆的几何参数

        :param Conductor_Radius: 导体半径
        :param EPR_Tape_Radius: EPR 绝缘带半径
        :param Insulation_Radius: 绝缘层半径
        :param Wrapping_Tape_Radius: 绕包带外半径
        :param Inner_Sheath_Radius: 内护套层半径
        :param Armor_Radius: 铠装层外半径
        :param Outer_Sheath_Radius: 外护套层外半径
        """
        pass  # 这里暂时不做任何计算，后续可以添加逻辑

    def JKEPJPM85_SC(Conductor_Radius, EPR_Tape_Radius, Insulation_Radius,
                     Wrapping_Tape_Radius, Inner_Sheath_Radius,
                     Armor_Radius, Outer_Sheath_Radius):
        """
        计算 JKEPJPM85_SC 电缆的几何参数

        :param Conductor_Radius: 导体半径
        :param EPR_Tape_Radius: EPR 绝缘带半径
        :param Insulation_Radius: 绝缘层半径
        :param Wrapping_Tape_Radius: 绕包带外半径
        :param Inner_Sheath_Radius: 内护套层半径
        :param Armor_Radius: 铠装层外半径
        :param Outer_Sheath_Radius: 外护套层外半径
        """
        pass  # 这里暂时不做任何计算，后续可以添加逻辑

    def JHEPJPM85_SC(Conductor_Radius, EPR_Tape_Radius, Insulation_Radius,
                     Wrapping_Tape_Radius, Inner_Sheath_Radius,
                     Armor_Radius, Outer_Sheath_Radius):
        """
        计算 JHEPJPM85_SC 电缆的几何参数

        :param Conductor_Radius: 导体半径
        :param EPR_Tape_Radius: EPR 绝缘带半径
        :param Insulation_Radius: 绝缘层半径
        :param Wrapping_Tape_Radius: 绕包带外半径
        :param Inner_Sheath_Radius: 内护套层半径
        :param Armor_Radius: 铠装层外半径
        :param Outer_Sheath_Radius: 外护套层外半径
        """
        pass  # 这里暂时不做任何计算，后续可以添加逻辑

    def JKMEHP8H_45(Conductor_Radius, EPR_Tape_Radius, Insulation_Radius,
                    Wrapping_Tape_Radius, Inner_Sheath_Radius,
                    Armor_Radius, Outer_Sheath_Radius):
        """
        计算 JKMEHP8H_45 电缆的几何参数

        :param Conductor_Radius: 导体半径
        :param EPR_Tape_Radius: EPR 绝缘带半径
        :param Insulation_Radius: 绝缘层半径
        :param Wrapping_Tape_Radius: 绕包带外半径
        :param Inner_Sheath_Radius: 内护套层半径
        :param Armor_Radius: 铠装层外半径
        :param Outer_Sheath_Radius: 外护套层外半径
        """
        pass  # 这里暂时不做任何计算，后续可以添加逻辑




