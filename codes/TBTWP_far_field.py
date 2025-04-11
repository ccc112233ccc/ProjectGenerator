import numpy as np
from numpy.linalg import inv
import matplotlib.pyplot as plt

def TBTWP_far_field(Lz, acc, pb, p, s, sb, rw, h, fmin, fmax, Np):
    """计算双绞线对远场特性
    
    Args:
        Lz (float): TBTWP总长度 (m)
        acc (float): 积分精度
        pb (float): 外层绞距 (m)
        p (float): 内层绞距 (m)
        s (float): 内层导线间距 (m)
        sb (float): 外层导线间距 (m)
        rw (float): 导线半径 (m)
        h (float): 高度 (m)
        fmin (float): 最小频率 (Hz)
        fmax (float): 最大频率 (Hz)
        Np (int): 频率点数
    
    Returns:
        tuple: (ICM1, IDM11, f) - 共模电流、差模电流和频率数组
    """
    # 自由空间特性
    u0 = 4 * np.pi * 1e-7    # 磁导率
    epsi = 8.85e-12          # 介电常数
    c0 = 299792458           # 真空光速
    etta0 = np.sqrt(u0/epsi)

    # 计算几何参数
    alpha_b = 1/np.sqrt((sb/2)**2 + (pb/(2*np.pi))**2)
    Lb = 2*np.pi*Lz/(alpha_b*pb)

    alpha = 1/np.sqrt((s/2)**2 + (p/(2*np.pi))**2)
    alpha0 = alpha_b*alpha*p/(2*np.pi)
    L = (2*np.pi)**2*Lz/(alpha_b*pb*alpha*p)

    l = np.arange(0, L+acc, acc)

    # 计算导线高度
    h11 = h + sb/2 + s/2
    h12 = h + sb/2 - s/2
    h21 = h - sb/2 + s/2
    h22 = h - sb/2 - s/2

    # 计算每单位长度参数
    L_11 = u0/(2*np.pi)*np.log((2*h/rw)-(s**2+sb**2)/(16*h**2))
    L_1112 = u0/(2*np.pi)*np.log((2*h/s)+(s**2+sb**2)/(16*h**2))
    L_1121 = u0/(4*np.pi)*np.log(1+4*h**2/sb**2)

    L_ = L_11
    L_M = L_1112
    L_12 = L_1121

    # 构建自感矩阵
    Lsh = np.array([
        [L_,   L_M,   L_12,  L_12],
        [L_M,  L_,    L_12,  L_12],
        [L_12, L_12,  L_,    L_M],
        [L_12, L_12,  L_M,   L_]
    ])

    Csh = c0**(-2) * inv(Lsh)
    Zc = c0 * Lsh

    # 构建阻抗矩阵
    Ra, Rb, Rc = 49, 51, 100
    Zsh_SL = np.array([
        [Ra+Rc, Rc,    0,     0],
        [Rc,    Rb+Rc, 0,     0],
        [0,     0,     Ra+Rc, Rc],
        [0,     0,     Rc,    Rb+Rc]
    ])
    Zsh_SR = Zsh_SL.copy()

    # 平面波参数
    E0 = 1
    thetaE = np.deg2rad(90)   # 极化角
    thetaP = np.deg2rad(0)    # 入射方向
    phiP = np.deg2rad(0)      # 入射方向

    ex = np.sin(thetaE)*np.sin(thetaP)
    ey = -np.sin(thetaE)*np.cos(thetaP)*np.cos(phiP)-np.cos(thetaE)*np.sin(phiP)
    ez = -np.sin(thetaE)*np.cos(thetaP)*np.sin(phiP)+np.cos(thetaE)*np.cos(phiP)

    # 计算导线位置
    x11 = h + (sb/2)*np.cos(alpha0*l) + s*np.cos(alpha*l)/2
    x12 = h + (sb/2)*np.cos(alpha0*l) - s*np.cos(alpha*l)/2
    x21 = h - (sb/2)*np.cos(alpha0*l) + s*np.cos(alpha*l)/2
    x22 = h - (sb/2)*np.cos(alpha0*l) - s*np.cos(alpha*l)/2

    y11 = (sb/2)*np.sin(alpha0*l) + s*np.sin(alpha*l)/2
    y12 = (sb/2)*np.sin(alpha0*l) - s*np.sin(alpha*l)/2
    y21 = -1*(sb/2)*np.sin(alpha0*l) + s*np.sin(alpha*l)/2
    y22 = -1*(sb/2)*np.sin(alpha0*l) - s*np.sin(alpha*l)/2

    z11 = pb*alpha_b*alpha*p*l/(2*np.pi)**2
    z12 = z11.copy()
    z21 = z11.copy()
    z22 = z11.copy()

    # 计算单位向量
    eta11 = np.sqrt(1 + s*sb*alpha*alpha0*np.cos(alpha0*l-alpha*l)/2)
    eta12 = np.sqrt(1 - s*sb*alpha*alpha0*np.cos(alpha0*l-alpha*l)/2)
    eta21 = eta12.copy()
    eta22 = eta11.copy()

    # 计算切向量分量
    n11_Lx = -1/eta11*(1/2*sb*alpha0*np.sin(alpha0*l)+1/2*s*alpha*np.sin(alpha*l))
    n11_Ly = 1/eta11*(1/2*sb*alpha0*np.cos(alpha0*l)+1/2*s*alpha*np.cos(alpha*l))
    n11_Lz = alpha0*pb/(2*np.pi*eta11)

    n12_Lx = -1/eta12*(1/2*sb*alpha0*np.sin(alpha0*l)-1/2*s*alpha*np.sin(alpha*l))
    n12_Ly = 1/eta12*(1/2*sb*alpha0*np.cos(alpha0*l)-1/2*s*alpha*np.cos(alpha*l))
    n12_Lz = alpha0*pb/(2*np.pi*eta12)

    n21_Lx = -1/eta21*(-1/2*sb*alpha0*np.sin(alpha0*l)+1/2*s*alpha*np.sin(alpha*l))
    n21_Ly = 1/eta21*(-1/2*sb*alpha0*np.cos(alpha0*l)+1/2*s*alpha*np.cos(alpha*l))
    n21_Lz = alpha0*pb/(2*np.pi*eta21)

    n22_Lx = -1/eta22*(1/2*sb*alpha0*np.sin(alpha0*l)+1/2*s*alpha*np.sin(alpha*l))
    n22_Ly = 1/eta22*(1/2*sb*alpha0*np.cos(alpha0*l)+1/2*s*alpha*np.cos(alpha*l))
    n22_Lz = alpha0*pb/(2*np.pi*eta22)

    # 频率循环
    frequencies = np.linspace(fmin, fmax, Np)
    IIout_0 = np.zeros((4, Np), dtype=complex)
    VVout_0 = np.zeros((4, Np), dtype=complex)

    for idx, f in enumerate(frequencies):
        k = 2*np.pi*f/c0
        kx = -k*np.cos(thetaP)
        ky = -k*np.sin(thetaP)*np.cos(phiP)
        kz = -k*np.sin(thetaP)*np.sin(phiP)

        # 计算电场分量
        Ex11 = 2*E0*ex*np.cos(kx*x11)*np.exp(-1j*(ky*y11+kz*z11))
        Ey11 = -2j*E0*ey*np.sin(kx*x11)*np.exp(-1j*(ky*y11+kz*z11))
        Ez11 = -2j*E0*ez*np.sin(kx*x11)*np.exp(-1j*(ky*y11+kz*z11))

        Ex12 = 2*E0*ex*np.cos(kx*x12)*np.exp(-1j*(ky*y12+kz*z12))
        Ey12 = -2j*E0*ey*np.sin(kx*x12)*np.exp(-1j*(ky*y12+kz*z12))
        Ez12 = -2j*E0*ez*np.sin(kx*x12)*np.exp(-1j*(ky*y12+kz*z12))

        Ex21 = 2*E0*ex*np.cos(kx*x21)*np.exp(-1j*(ky*y21+kz*z21))
        Ey21 = -2j*E0*ey*np.sin(kx*x21)*np.exp(-1j*(ky*y21+kz*z21))
        Ez21 = -2j*E0*ez*np.sin(kx*x21)*np.exp(-1j*(ky*y21+kz*z21))

        Ex22 = 2*E0*ex*np.cos(kx*x22)*np.exp(-1j*(ky*y22+kz*z22))
        Ey22 = -2j*E0*ey*np.sin(kx*x22)*np.exp(-1j*(ky*y22+kz*z22))
        Ez22 = -2j*E0*ez*np.sin(kx*x22)*np.exp(-1j*(ky*y22+kz*z22))

        # 计算总电场
        E11 = Ex11*n11_Lx + Ey11*n11_Ly + Ez11*n11_Lz
        E12 = Ex12*n12_Lx + Ey12*n12_Ly + Ez12*n12_Lz
        E21 = Ex21*n21_Lx + Ey21*n21_Ly + Ez21*n21_Lz
        E22 = Ex22*n22_Lx + Ey22*n22_Ly + Ez22*n22_Lz

        E = np.vstack([E11, E12, E21, E22])

        # 计算传输矩阵
        PHI11 = np.cos(k*L)*np.eye(4)
        PHI12 = -1j*Zc*np.sin(k*L)
        PHI21 = -1j*inv(Zc)*np.sin(k*L)
        PHI22 = np.cos(k*L)*np.eye(4)
        Zcinv = inv(Zc)

        # 计算感应源
        VAG = np.zeros(4, dtype=complex)
        IAG = np.zeros(4, dtype=complex)

        for i in range(4):
            VAG[i] = np.trapezoid(np.cos(k*(L-l))*E[i,:], l)
            IAG[i] = sum(np.trapezoid(-1j*Zcinv[i,j]*np.sin(k*(L-l))*E[j,:], l) 
                        for j in range(4))

        # 计算端口电压
        n11 = np.arange(0, h11+acc, acc)
        n12 = np.arange(0, h12+acc, acc)
        n21 = np.arange(0, h21+acc, acc)
        n22 = np.arange(0, h22+acc, acc)

        Vinc01 = -np.trapezoid(2*E0*ex*np.cos(kx*n11)*np.exp(-1j*(ky*y11[0]+kz*0)), n11)
        Vinc02 = -np.trapezoid(2*E0*ex*np.cos(kx*n12)*np.exp(-1j*(ky*y12[0]+kz*0)), n12)
        Vinc03 = -np.trapezoid(2*E0*ex*np.cos(kx*n21)*np.exp(-1j*(ky*y21[0]+kz*0)), n21)
        Vinc04 = -np.trapezoid(2*E0*ex*np.cos(kx*n22)*np.exp(-1j*(ky*y22[0]+kz*0)), n22)

        VincL1 = -np.trapezoid(2*E0*ex*np.cos(kx*n11)*np.exp(-1j*(ky*y11[-1]+kz*L)), n11)
        VincL2 = -np.trapezoid(2*E0*ex*np.cos(kx*n12)*np.exp(-1j*(ky*y12[-1]+kz*L)), n12)
        VincL3 = -np.trapezoid(2*E0*ex*np.cos(kx*n21)*np.exp(-1j*(ky*y21[-1]+kz*L)), n21)
        VincL4 = -np.trapezoid(2*E0*ex*np.cos(kx*n22)*np.exp(-1j*(ky*y22[-1]+kz*L)), n22)

        Vinc0 = np.array([Vinc01, Vinc02, Vinc03, Vinc04])
        VincL = np.array([VincL1, VincL2, VincL3, VincL4])

        VST = VAG + VincL - PHI11@Vinc0
        IST = IAG - PHI21@Vinc0

        # 计算频率相关矩阵
        A = PHI11@Zsh_SL + Zsh_SR@PHI22 - PHI12 - Zsh_SR@PHI21@Zsh_SL

        # 计算输出电流和电压
        Iout_0 = np.linalg.solve(A, VST - Zsh_SR@IST)
        IIout_0[:,idx] = Iout_0
        VVout_0[:,idx] = -Zsh_SL@Iout_0

    # 计算共模和差模电流
    ICM1 = IIout_0[0,:] + IIout_0[1,:]
    IDM11 = (IIout_0[0,:] - IIout_0[1,:])/2

    return ICM1, IDM11, frequencies

if __name__ == "__main__":
    # 测试参数
    Lz = 1         # 总长度
    acc = 1e-4     # 精度
    pb = 25e-3     # 外层绞距
    p = 5e-3       # 内层绞距
    s = 0.7e-3     # 内层导线间距
    sb = 1.5e-3    # 外层导线间距
    rw = 0.15e-3   # 导线半径
    h = 5e-3       # 高度
    fmin = 1e6     # 最小频率
    fmax = 1e9     # 最大频率
    Np = 201       # 频率点数

    # 运行计算
    ICM1, IDM11, f = TBTWP_far_field(Lz, acc, pb, p, s, sb, rw, h, fmin, fmax, Np)

    # 计算幅值
    gcm = 20*np.log10(np.abs(ICM1))
    hdm = 20*np.log10(np.abs(IDM11))

    # 绘图
    plt.figure(figsize=(10, 6))
    plt.semilogx(f, gcm, '--', linewidth=2, label='CM')
    plt.semilogx(f, hdm, linewidth=2, label='DM')
    plt.grid(True)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Modal Current (dBA)')
    plt.legend()
    plt.title('TBTWP Far Field Response')
    plt.show()