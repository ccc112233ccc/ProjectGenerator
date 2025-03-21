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

    @staticmethod
    def JEPJ85_NSC(Conductor_Radius, Mica_Tape_Radius, Insulation_Radius, Wrapping_Tape_Radius,
                   Inner_Sheath_Radius, Armor_Radius, Outer_Sheath_Radius):
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




