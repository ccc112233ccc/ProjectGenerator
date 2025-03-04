import matlab.engine
import numpy as np


def call_matlab_function(rw, rsh, epsir, TanLoss, tsh, Lz, segmaAL, segmaCu, xd1, xd2, slot_d, fmin, fmax, Np):
    eng = matlab.engine.start_matlab()
    s_params2, sscd21, sscd11, sscc21, sscc11, ssdd21, ssdd11, f = eng.zhaolong_twinax_cable_oussama_1(
        rw, rsh, epsir, TanLoss, tsh, Lz, segmaAL, segmaCu, xd1, xd2, slot_d, fmin, fmax, Np, nargout=8
    )
    eng.quit()
    return s_params2, sscd21, sscd11, sscc21, sscc11, ssdd21, ssdd11, f


def save_results_to_file(results, filename):
    s_params2, sscd21, sscd11, sscc21, sscc11, ssdd21, ssdd11, f = results
    np.savez(filename, s_params2=s_params2, sscd21=sscd21, sscd11=sscd11,
             sscc21=sscc21, sscc11=sscc11, ssdd21=ssdd21, ssdd11=ssdd11, f=f)


def save_results_to_csv(results, filename_prefix):
    s_params2, sscd21, sscd11, sscc21, sscc11, ssdd21, ssdd11, f = results
    # np.savetxt(f"{filename_prefix}_s_params2.csv", s_params2, delimiter=",")
    np.savetxt(f"{filename_prefix}_sscd21.csv", sscd21, delimiter=",")
    np.savetxt(f"{filename_prefix}_sscd11.csv", sscd11, delimiter=",")
    np.savetxt(f"{filename_prefix}_sscc21.csv", sscc21, delimiter=",")
    np.savetxt(f"{filename_prefix}_sscc11.csv", sscc11, delimiter=",")
    np.savetxt(f"{filename_prefix}_ssdd21.csv", ssdd21, delimiter=",")
    np.savetxt(f"{filename_prefix}_ssdd11.csv", ssdd11, delimiter=",")
    np.savetxt(f"{filename_prefix}_f.csv", f, delimiter=",")


# Example usage
if __name__ == "__main__":
    rw = 0.415e-3 / 2
    rsh = 1.42e-3
    epsir = 2
    TanLoss = 5e-4
    tsh = 9e-6
    Lz = 0.2
    segmaAL = 38160000
    segmaCu = 58130000
    xd1 = 1.42e-3 / 2 + 0.05 * 1.42e-3 / 2
    xd2 = -1.42e-3 / 2
    slot_d = 0.07e-3
    fmin = 1e6
    fmax = 1e9
    Np = 100

    results = call_matlab_function(
        rw, rsh, epsir, TanLoss, tsh, Lz, segmaAL, segmaCu, xd1, xd2, slot_d, fmin, fmax, Np)
    save_results_to_csv(results, 'results')
    print("Results saved to CSV files")
