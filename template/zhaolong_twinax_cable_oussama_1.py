import matlab.engine
import numpy as np
import pandas as pd
import fire


def call_matlab_function(rw, rsh, epsir, TanLoss, tsh, Lz, segmaAL, segmaCu, slot_d, fmin, fmax, Np):
    eng = matlab.engine.start_matlab()
    s_params2, sscd21, sscd11, sscc21, sscc11, ssdd21, ssdd11, f = eng.zhaolong_twinax_cable_oussama_1(
        rw, rsh, epsir, TanLoss, tsh, Lz, segmaAL, segmaCu, slot_d, fmin, fmax, Np, nargout=8
    )
    eng.quit()
    return s_params2, sscd21, sscd11, sscc21, sscc11, ssdd21, ssdd11, f


def save_results_to_csv(results, filename):
    s_params2, sscd21, sscd11, sscc21, sscc11, ssdd21, ssdd11, f = results
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
    df.to_csv(f"{filename}", index=False)


def zhaolong_twinax_cable_oussama_1(rw: float = 0.2075e-3, rsh: float = 1.42e-3, epsir: float = 2, TanLoss: float = 5e-4, tsh: float = 9e-6, Lz: float = 0.2, segmaAL: float = 38160000, segmaCu: float = 58130000, slot_d: float = 0.07e-3, fmin: float = 1e9, fmax: float = 10e9, Np: int = 500, filename: str = "results"):
    results = call_matlab_function(
        rw, rsh, epsir, TanLoss, tsh, Lz, segmaAL, segmaCu, slot_d, fmin, fmax, Np)
    save_results_to_csv(results, filename)


def zhaolong_twinax_cable_oussama_1_cli():
    fire.Fire(zhaolong_twinax_cable_oussama_1)


def zhaolong_twinax_cable_oussama_1_from_json(json_path: str):
    import json
    with open(json_path, "r", encoding="utf-8") as f:
        params = json.load(f)
    rw = params["导体半径"]
    rsh = params["绝缘体半径"]
    epsir = params["绝缘体相对介电常数"]
    TanLoss = params["绝缘体损耗正切"]
    tsh = params["屏蔽层厚度"]
    Lz = params["线缆长度"]
    segmaAL = params["屏蔽层电导率"]
    segmaCu = params["导体电导率"]
    slot_d = params["屏蔽层厚度"]

    fmin = params["频率最小值"]
    fmax = params["频率最大值"]
    Np = params["频率点数"]
    filename = params["结果文件"]
    zhaolong_twinax_cable_oussama_1(
        rw, rsh, epsir, TanLoss, tsh, Lz, segmaAL, segmaCu, slot_d, fmin, fmax, Np, filename)


if __name__ == "__main__":
    zhaolong_twinax_cable_oussama_1_from_json("./template/current.json")
