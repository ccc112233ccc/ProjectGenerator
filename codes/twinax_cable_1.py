import numpy as np
from scipy.special import ive, kve  # besseli 和 besselk 函数
from scipy.linalg import expm    # matrix exponential
from scipy.linalg import block_diag
def twinax_cable_1(rw, D, rsh, epsir, TanLoss, tsh, Lz, segmaAL, segmaCu, slot_d, fmin, fmax, Np):
    """双轴电缆传输线模型计算函数
    
    Args:
        rw (float): 内导线半径 (m)
        D (float): 信号线间距 (m)
        rsh (float): 屏蔽半径 (m)
        epsir (float): 介质常数
        TanLoss (float): 介质损耗正切
        tsh (float): 屏蔽厚度 (m)
        Lz (float): 同轴线缆总长度 (m)
        segmaAL (float): 屏蔽导电率 (S/m)
        segmaCu (float): 导线导电率 (S/m)
        slot_d (float): 缝隙尺寸 (m)
        fmin (float): 最小频率 (Hz)
        fmax (float): 最大频率 (Hz)
        Np (int): 频率点数
    """
    # 基本常数
    u0 = 4 * np.pi * 1e-7      # 真空磁导率 (H/m)
    epsi = 8.85e-12            # 真空介电常数 (F/m)
    c0 = 299792458            # 真空中光速 (m/s)

    # 计算参数
    xd1 = D/2 + 0.05*D/2      # 内导体1相对于轴线的偏移
    xd2 = -D/2                # 内导体2相对于轴线的偏移

    # 内系统平均每单位长度参数计算
    Delta1 = (rw**2 - xd1**2 - rsh**2)**2 - 4*(xd1*rsh)**2
    alpha1 = (-(rw**2 - xd1**2 - rsh**2) - np.sqrt(Delta1)) / (2*xd1*rsh)
    F1 = 1 / (np.pi * np.log(alpha1*(alpha1*xd1 - rsh) / (xd1 - alpha1*rsh)))

    Delta2 = (rw**2 - xd2**2 - rsh**2)**2 - 4*(xd2*rsh)**2
    alpha2 = (-(rw**2 - xd2**2 - rsh**2) - np.sqrt(Delta2)) / (2*xd2*rsh)
    F2 = 1 / (np.pi * np.log(alpha2*(alpha2*xd2 - rsh) / (xd2 - alpha2*rsh)))

    # 计算自感
    Lin11 = u0/(2*np.pi) * np.log((rsh**2 - xd1**2) / (rsh * rw))
    Lin22 = u0/(2*np.pi) * np.log((rsh**2 - xd2**2) / (rsh * rw))
    Lin12 = u0/(2*np.pi) * np.log((1/rsh)*np.sqrt(((xd1*xd2)**2+rsh**4+2*abs(xd1*xd2)*rsh**2)/((xd1)**2+xd2**2+2*abs(xd1*xd2))))

    # 内导体1附加参数
    delta_val = (rw**2 - xd1**2 - rsh**2)**2 - 4*(xd1*rsh)**2
    phi_a = np.deg2rad(0)
    alpha11 = xd1 / rsh if xd1 == 0 else (-(rw**2 - xd1**2 - rsh**2) - np.sqrt(delta_val)) / (2*xd1*rsh)
    N_val = np.log((rsh**2 - xd1**2) / (rw * rsh)) / (2*np.pi)
    A1 = (1 - alpha11**2) / (1 + alpha11**2 - 2*alpha11*np.cos(phi_a))
    La1 = u0/np.pi * (slot_d/(4*rsh))**2 * A1**2
    Ca1 = epsi*epsir/np.pi * (slot_d/(4*rsh*N_val))**2 * A1**2

    # 内导体2附加参数
    delta_val = (rw**2 - xd2**2 - rsh**2)**2 - 4*(xd2*rsh)**2
    alpha22 = xd2 / rsh if xd2 == 0 else (-(rw**2 - xd2**2 - rsh**2) - np.sqrt(delta_val)) / (2*xd2*rsh)
    N_val = np.log((rsh**2 - xd2**2) / (rw * rsh)) / (2*np.pi)
    A2 = (1 - alpha22**2) / (1 + alpha22**2 - 2*alpha22*np.cos(phi_a))
    La2 = u0/np.pi * (slot_d/(4*rsh))**2 * A2**2
    Ca2 = epsi*epsir/np.pi * (slot_d/(4*rsh*N_val))**2 * A2**2

    # 总自感与电容矩阵
    LT = np.array([[Lin11, Lin12], [Lin12, Lin22]]) + np.array([[La1, 0], [0, La2]])
    CT = (c0**-2) * np.linalg.inv(LT) * epsir * (1 - 1j*TanLoss) - np.array([[Ca1, 0], [0, Ca2]])

    # 频率循环
    frequencies = np.linspace(fmin, fmax, Np)
    ChainA = np.zeros((4, 4, Np), dtype=complex)

    for idx, freq in enumerate(frequencies):
        # 内导体1部分计算
        delta_val = 1 / np.sqrt(np.pi * freq * u0 * segmaCu)
        beta = (1 + 1j) / delta_val
        Zac = (beta / (2*np.pi*segmaCu*rw)) * ive(0, beta*rw) / ive(1, beta*rw)
        Delta = (rw**2 - xd1**2 - rsh**2)**2 - 4*(xd1*rsh)**2
        alpha_val = (-(rw**2 - xd1**2 - rsh**2) - np.sqrt(Delta)) / (2*xd1*rsh) if xd1 != 0 else 0
        factor1 = 1 if xd1 == 0 else alpha_val * (rsh**2 - rw**2 - xd1**2) / (rsh*xd1*(1 - alpha_val**2))
        CT1 = Zac * factor1

        # 内导体2部分计算
        delta_val = 1 / np.sqrt(np.pi * freq * u0 * segmaCu)
        beta = (1 + 1j) / delta_val
        Zac = (beta / (2*np.pi*segmaCu*rw)) * ive(0, beta*rw) / ive(1, beta*rw)
        Delta = (rw**2 - xd2**2 - rsh**2)**2 - 4*(xd2*rsh)**2
        alpha_val = (-(rw**2 - xd2**2 - rsh**2) - np.sqrt(Delta)) / (2*xd2*rsh) if xd2 != 0 else 0
        factor2 = 1 if xd2 == 0 else alpha_val * (rsh**2 - rw**2 - xd2**2) / (rsh*xd2*(1 - alpha_val**2))
        CT2 = Zac * factor2

        # 盾层部分计算
        delta_val = 1 / np.sqrt(np.pi * freq * u0 * segmaAL)
        beta = (1 + 1j) / delta_val
        
        DELTA1 = (rw**2 - xd1**2 - rsh**2)**2 - 4*(xd1*rsh)**2
        DELTA2 = (rw**2 - xd2**2 - rsh**2)**2 - 4*(xd2*rsh)**2
        
        alpha_sh1 = 0 if xd1 == 0 else (-(rw**2 - xd1**2 - rsh**2) - np.sqrt(DELTA1)) / (2*xd1*rsh)
        alpha_sh2 = 0 if xd2 == 0 else (-(rw**2 - xd2**2 - rsh**2) - np.sqrt(DELTA2)) / (2*xd2*rsh)

        # 计算贝塞尔函数相关项
        factor_sh = (-ive(1, beta*rsh) * kve(1, beta*(rsh+tsh)) * 
                    np.exp(abs(np.real(beta*rsh)) - beta*(rsh+tsh)) + 
                    ive(1, beta*(rsh+tsh)) * kve(1, beta*rsh) * 
                    np.exp(abs(np.real(beta*(rsh+tsh))) - beta*rsh))
        
        F_sh = (kve(1, beta*(rsh+tsh)) * ive(0, beta*rsh) * 
                np.exp(abs(np.real(beta*rsh)) - beta*(rsh+tsh)) + 
                ive(1, beta*(rsh+tsh)) * kve(0, beta*rsh) * 
                np.exp(abs(np.real(beta*(rsh+tsh))) - beta*rsh))

        Ainsh = beta * F_sh / (2*np.pi * segmaAL * rsh * factor_sh)
        Ainsh11 = Ainsh * (1 + alpha_sh1**2) / (1 - alpha_sh1**2)
        Binsh22 = Ainsh * (1 + alpha_sh2**2) / (1 - alpha_sh2**2)
        Cinsh12 = Ainsh * (alpha_sh1*(1 - alpha_sh2**2) - alpha_sh2*(1 - alpha_sh1**2)) / (alpha_sh1*(1 + alpha_sh2**2) - alpha_sh2*(1 + alpha_sh2))

        # 构建阻抗矩阵
        AA = np.array([[Ainsh11, Cinsh12], [Cinsh12, Binsh22]]) + np.array([[CT1, 0], [0, CT2]])
        Z = AA + 1j*2*np.pi*freq*LT
        Y = 1j*2*np.pi*freq*CT
        
        # 计算链参数矩阵
        A_matrix = -np.block([[np.zeros((2,2)), Z], [Y, np.zeros((2,2))]])
        ChainA[:,:,idx] = expm(-A_matrix * Lz)

    # 转换为S参数（需要实现abcd2s和s2smm函数）
    s_params2 = abcd2s(ChainA, 50)
    SDD, SDC, SCD, SCC = s2smm(s_params2, 2)
    
    ssdd11 = SDD[0,0,:]
    ssdd21 = SDD[1,0,:]
    sscc11 = SCC[0,0,:]
    sscc21 = SCC[1,0,:]
    sscd11 = SCD[0,0,:]
    sscd21 = SCD[1,0,:]

    return s_params2, sscd21, sscd11, sscc21, sscc11, ssdd21, ssdd11, frequencies

def abcd2s(abcd_params, z0=50):
    """
    Convert ABCD-parameters to S-parameters.

    Parameters:
    -----------
    abcd_params : ndarray
        3D complex array of shape (2N, 2N, M), where M is number of frequency points.
    z0 : float or 1D array-like, optional
        Reference impedance (can be scalar or array of length M). Default is 50.

    Returns:
    --------
    s_params : ndarray
        3D complex array of shape (2N, 2N, M) containing the S-parameters.
    """
    abcd_params = np.asarray(abcd_params)
    n_ports = abcd_params.shape[0] // 2
    n_freqs = abcd_params.shape[2]

    # Ensure z0 is an array of correct shape
    if np.isscalar(z0):
        z0 = np.full(n_freqs, z0, dtype=float)
    else:
        z0 = np.asarray(z0)
        assert len(z0) == n_freqs, "z0 must match number of frequency points"
    if np.any(np.iscomplex(z0)):
        raise ValueError("z0 must be real-valued")

    s_params = np.zeros_like(abcd_params, dtype=complex)

    I = np.eye(n_ports)

    for k in range(n_freqs):
        A = abcd_params[0:n_ports, 0:n_ports, k]
        B = abcd_params[0:n_ports, n_ports:2 * n_ports, k]
        C = abcd_params[n_ports:2 * n_ports, 0:n_ports, k]
        D = abcd_params[n_ports:2 * n_ports, n_ports:2 * n_ports, k]
        Z0k = z0[k]

        # 标准公式修正
        denom = A + B / Z0k + C * Z0k + D
        denom_inv = np.linalg.inv(denom)
        S11 = (A + B / Z0k - C * Z0k - D) @ denom_inv
        S12 = 2 * (A @ denom_inv)
        S21 = 2 * denom_inv
        S22 = (-A + B / Z0k - C * Z0k + D) @ denom_inv

        # 赋值修正
        s_params[0:n_ports, 0:n_ports, k] = S11
        s_params[0:n_ports, n_ports:2 * n_ports, k] = S12
        s_params[n_ports:2 * n_ports, 0:n_ports, k] = S21
        s_params[n_ports:2 * n_ports, n_ports:2 * n_ports, k] = S22
    return s_params
def s2smm(s_params, rfflag=1):
    s_params = np.asarray(s_params)
    N = s_params.shape[0]
    pts = s_params.shape[2]

    if N % 2 != 0:
        raise ValueError("Only even-port networks are supported in this implementation.")

    if rfflag == 1:
        Ports = list(range(0, N, 2)) + list(range(1, N, 2))
    elif rfflag == 2:
        Ports = list(range(N))
    elif rfflag == 3:
        Ports = list(range(N // 2)) + list(range(N - 1, N // 2 - 1, -1))
    else:
        raise ValueError("Invalid rfflag. Use 1, 2, or 3.")

    s_params = s_params[np.ix_(Ports, Ports, range(pts))]

    # 正确构建 M = [ [1 -1]; [1 1] ] 的块对角结构
    m_diff = np.array([[1, -1]])
    m_comm = np.array([[1, 1]])

    M1 = block_diag(*([m_diff] * (N // 2)))
    M2 = block_diag(*([m_comm] * (N // 2)))
    M = np.vstack((M1, M2))
    invM = M.T

    smm_params = np.zeros_like(s_params, dtype=complex)
    for idx in range(pts):
        smm_params[:, :, idx] = M @ s_params[:, :, idx] @ invM / 2

    N_half = N // 2
    SDD = smm_params[0:N_half, 0:N_half, :]
    SDC = smm_params[0:N_half, N_half:N, :]
    SCD = smm_params[N_half:N, 0:N_half, :]
    SCC = smm_params[N_half:N, N_half:N, :]

    return SDD, SDC, SCD, SCC


if __name__ == "__main__":
#  %%%%% Cable Parameters (部分默认值已注释) %%%%%
#     % rw   = 0.415e-3/2;    % 内导线半径 (m)
#     % D    = 1.42e-3;       % 信号线间距 (m)
#     % h0   = D;            % 屏蔽与内导体距离 (m)
#     % rsh  = h0;           % 屏蔽半径
#     % epsir = 2;           % 介质常数
#     % TanLoss = 5e-4;      % 介质损耗正切
#     % tsh  = 9e-6;         % 屏蔽厚度 (m)
#     % Lz   = 0.2;          % 同轴线缆总长度 (m)
#     % segmaAL = 38160000;  % 屏蔽导电率 (S/m)
#     % segmaCu = 58130000;  % 导线导电率 (S/m)
#     xd1  = D/2 + 0.05*D/2; % 内导体1相对于轴线的偏移
#     xd2  = -D/2;         % 内导体2相对于轴线的偏移
#     % slot_d = 0.07e-3;     % 缝隙尺寸
#     % fmin = 1e9;          % 最小频率 (Hz)
#     % fmax = 20e9;         % 最大频率 (Hz)

#     % Np   = 1000;         % 频率点数
    rw = 0.415e-3/2
    D = 1.42e-3
    h0 = D
    rsh = h0
    epsir = 2   
    TanLoss = 5e-4
    tsh = 9e-6
    Lz = 0.2
    segmaAL = 38160000
    segmaCu = 58130000
    xd1 = D/2 + 0.05*D/2
    xd2 = -D/2
    slot_d = 0.07e-3
    fmin = 1e9
    fmax = 20e9
    Np = 1000

    # 调用函数计算
    s_params2, sscd21, sscd11, sscc21, sscc11, ssdd21, ssdd11, frequencies = twinax_cable_1(rw, D, rsh, epsir, TanLoss, tsh, Lz, segmaAL, segmaCu, slot_d, fmin, fmax, Np)

    # 打印结果
    import matplotlib.pyplot as plt

    plt.plot(frequencies, 20 * np.log10(np.abs(sscd21)), label='S21')
    plt.show()