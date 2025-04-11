import numpy as np
import matplotlib.pyplot as plt

def star_quad_cable(s, h, rw, p, Lz, fmin, fmax, Np):
    """星型四绞线电缆分析函数
    
    Args:
        s (float): 导线间距
        h (float): 高度
        rw (float): 导线半径
        p (float): 节距
        Lz (float): 总长度
        fmin (float): 最小频率
        fmax (float): 最大频率
        Np (int): 频率点数
    
    Returns:
        tuple: (ICM, IDM2, f) - 共模电流、差模电流和频率数组
    """
    # 自由空间特性
    u0 = 4 * np.pi * 1e-7    # 磁导率
    epsi = 8.85e-12          # 介电常数
    c0 = 299792458           # 真空光速
    etta0 = np.sqrt(u0/epsi)

    # 星型四绞线参数计算
    alpha = ((s/2)**2 + (p/(2*np.pi))**2)**(-1/2)
    L = 2*np.pi*Lz/alpha/p

    # 平均每单位长度参数
    Ls = u0/(2*np.pi)*(np.log(2*h/rw)-s**2/(16*h**2))
    L12 = u0/(2*np.pi)*(np.log(2*h/(s*abs(np.sin(np.pi/4))))-s**2/(16*h**2)*np.cos(np.pi/2))
    L13 = u0/(2*np.pi)*(np.log(2*h/(s*abs(np.sin(np.pi/2))))-s**2/(16*h**2)*np.cos(np.pi))
    LM = np.array([
        [Ls,  L12, L13, L12],
        [L12, Ls,  L12, L13],
        [L13, L12, Ls,  L12],
        [L12, L13, L12, Ls]
    ])
    Zc = c0*LM

    # 阻抗参数
    Ra, Rb, Rc = 100, 100, 100
    v = np.array([Ra, Rb, Ra, Rb])
    Zl = Rc*np.ones((4,4)) + np.diag(v)
    Zs = Zl.copy()

    # 自感矩阵
    LLS = np.array([
        [9.733, 9.190, 8.822, 9.189],
        [9.191, 9.323, 8.770, 8.901],
        [8.822, 8.770, 8.897, 8.769],
        [9.189, 8.901, 8.769, 9.320]
    ]) * 1e-9
    LRS = LLS.copy()

    # 变换矩阵
    TV = np.array([
        [1/4,  1/4,   1/4,   1/4],
        [1/2, -1/2,   1/2,  -1/2],
        [1,     0,    -1,     0],
        [0,     1,     0,    -1]
    ])
    TI = np.array([
        [1,    1,    1,    1],
        [1/2, -1/2,  1/2, -1/2],
        [1/2,  0,   -1/2,  0],
        [0,    1/2,  0,   -1/2]
    ])

    # 平面波参数
    E0 = 1
    thetaE = np.deg2rad(0)
    thetaP = np.deg2rad(0)
    phiP = np.deg2rad(0)

    ex = np.sin(thetaE)*np.sin(thetaP)
    ey = -np.sin(thetaE)*np.cos(thetaP)*np.cos(phiP)-np.cos(thetaE)*np.sin(phiP)
    ez = -np.sin(thetaE)*np.cos(thetaP)*np.sin(phiP)+np.cos(thetaE)*np.cos(phiP)

    # 扭绞几何参数
    acc = 1e-5
    l = np.arange(0, L+acc, acc)
    VSL = np.zeros((4, Np), dtype=complex)
    VSR = np.zeros((4, Np), dtype=complex)
    
    frequencies = np.linspace(fmin, fmax, Np)
    
    for i in range(4):
        x = h + np.cos(alpha*l + (i)*np.pi/2)*(s/2)
        dx = -alpha*np.sin(alpha*l + (i)*np.pi/2)*(s/2)
        y = np.sin(alpha*l + (i)*np.pi/2)*(s/2)
        dy = alpha*np.cos(alpha*l + (i)*np.pi/2)*(s/2)
        z = alpha*l*p/(2*np.pi)
        dz = alpha*p/(2*np.pi)

        for idx, f in enumerate(frequencies):
            k = 2*np.pi*f/c0
            kx = -k*np.cos(thetaP)
            ky = -k*np.sin(thetaP)*np.cos(phiP)
            kz = -k*np.sin(thetaP)*np.sin(phiP)
            
            Ex = 2*E0*ex*np.cos(kx*x)*np.exp(-1j*(ky*y+kz*z))
            Ey = -2j*E0*ey*np.sin(kx*x)*np.exp(-1j*(ky*y+kz*z))
            Ez = -2j*E0*ez*np.sin(kx*x)*np.exp(-1j*(ky*y+kz*z))
            
            VF = Ex*dx + Ey*dy + Ez*dz
            SNC1 = np.sin(k*(l-L))/np.sin(k*L)
            SNC2 = np.sin(k*l)/np.sin(k*L)
            
            vSLl = np.trapezoid(SNC1*VF, l)
            vSRl = np.trapezoid(SNC2*VF, l)
            
            vSLv = -2*E0*ex*np.sin(kx*x[0])/kx
            vSRv = -2*E0*ex*np.sin(kx*x[-1])*np.exp(-1j*(ky*y[-1]+kz*Lz))/kx
            
            VSL[i,idx] = vSLl + vSLv
            VSR[i,idx] = vSRl + vSRv

    # 频率循环计算
    I0 = np.zeros((4, Np), dtype=complex)
    for idx, f in enumerate(frequencies):
        k = 2*np.pi*f/c0
        w = 2*np.pi*f
        
        # 频率相关矩阵
        PHI11 = np.cos(k*L)*np.eye(4)
        PHI12 = -1j*Zc*np.sin(k*L)
        PHI21 = -1j*np.linalg.inv(Zc)*np.sin(k*L)
        PHI22 = np.cos(k*L)*np.eye(4)
        
        Zs1 = Zs + 1j*w*LLS
        Zl1 = Zl + 1j*w*LRS
        
        D = PHI11@Zs + Zl@PHI22 - Zl@PHI21@Zs - PHI12
        I0[:,idx] = np.linalg.solve(D, (Zs@PHI21 - PHI11)@VSL[:,idx] + VSR[:,idx])

    R = TI@I0
    ICM = R[0,:]
    IDM2 = R[1,:]

    return ICM, IDM2, frequencies

if __name__ == "__main__":
    # 测试参数
    s = 2.5e-3    # 导线间距
    h = 1e-2      # 高度
    rw = 0.25e-3  # 导线半径
    p = 5e-2      # 节距
    Lz = 1        # 总长度
    fmin = 1e6    # 最小频率
    fmax = 1e9    # 最大频率
    Np = 201      # 频率点数
    
    ICM, IDM2, f = star_quad_cable(s, h, rw, p, Lz, fmin, fmax, Np)