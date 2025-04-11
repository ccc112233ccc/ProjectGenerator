import numpy as np
import matplotlib.pyplot as plt

def TWP_far_field(s, h, rw, p, Lz, fmin, fmax, Np):
    """计算双绞线远场特性
    
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
        tuple: (CMC, DMC, f) - 共模电流、差模电流和频率数组
    """
    # 自由空间特性
    u0 = 4 * np.pi * 1e-7    # 磁导率
    epsi = 8.85e-12          # 介电常数
    c0 = 299792458           # 真空光速

    # 扭绞束参数
    alpha = ((s/2)**2 + (p/(2*np.pi))**2)**(-1/2)
    L = 2*np.pi*Lz/alpha/p

    # 平均每单位长度参数
    Ra, Rb, Rc = 50, 50, 100
    l_avg = u0/(2*np.pi) * np.log(2*h/rw)
    lm_avg = u0/(2*np.pi) * (np.log(2*h/s) + s**2/(16*h**2))
    L_avg = np.array([[l_avg, lm_avg], [lm_avg, l_avg]])
    C_avg = (1/(c0**2)) * L_avg
    Zc = c0 * L_avg

    Zl = np.array([[Ra+Rc, Rc], [Rc, Rb+Rc]])
    Zs = Zl.copy()

    Zc_vr = c0*u0/(2*np.pi) * (np.log(2*h/rw) - 1)
    L_vr = h*Zc_vr/c0
    Zc_dr = c0*u0/(2*np.pi) * np.log(s/rw)

    # 平面波特性
    E0 = 1
    # End-Fire configuration
    thetaE = np.deg2rad(90)
    thetaP = np.deg2rad(90)
    phiP = np.deg2rad(-90)

    ex = np.sin(thetaE)*np.sin(thetaP)
    ey = -np.sin(thetaE)*np.cos(thetaP)*np.cos(phiP)-np.cos(thetaE)*np.sin(phiP)
    ez = -np.sin(thetaE)*np.cos(thetaP)*np.sin(phiP)+np.cos(thetaE)*np.cos(phiP)

    # 扭绞几何参数
    acc = 1e-5
    l = np.arange(0, L+acc, acc)
    frequencies = np.linspace(fmin, fmax, Np)
    VSL = np.zeros((2, Np), dtype=complex)
    VSR = np.zeros((2, Np), dtype=complex)

    for i in range(2):
        x = h + (np.cos(alpha*l)*(s/2)*((-1)**(i)))
        dx = -(alpha*np.sin(alpha*l)*(s/2)*((-1)**(i)))
        y = np.sin(alpha*l)*(s/2)*((-1)**(i))
        dy = alpha*np.cos(alpha*l)*(s/2)*(-1)**(i)
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
    I0 = np.zeros((2, Np), dtype=complex)
    for idx, f in enumerate(frequencies):
        k = 2*np.pi*f/c0
        
        PHI11 = np.cos(k*L)*np.eye(2)
        PHI12 = -1j*Zc*np.sin(k*L)
        PHI21 = -1j*np.linalg.inv(Zc)*np.sin(k*L)
        PHI22 = np.cos(k*L)*np.eye(2)
        
        Zr = Zc_vr*(0+1j*Zc_vr*np.tan(k*h))/(Zc_vr+1j*0*np.tan(k*h))
        Zl1 = Zl + Zr*np.ones((2,2))
        Zs1 = Zl1.copy()
        
        D = PHI11@Zs + Zl@PHI22 - Zl@PHI21@Zs - PHI12
        I0[:,idx] = np.linalg.solve(D, (Zs@PHI21 - PHI11)@VSL[:,idx] + VSR[:,idx])

    # 计算远场
    CMC = I0[0,:] + I0[1,:]
    DMC = (I0[0,:] - I0[1,:])/2

    return CMC, DMC, frequencies

if __name__ == "__main__":
    # 测试参数
    s = 0.25e-2   # 导线间距
    h = 1e-2      # 高度
    rw = 1.46e-9  # 导线半径
    p = 5e-2      # 节距
    Lz = 1        # 总长度
    fmin = 1e6    # 最小频率
    fmax = 1e9    # 最大频率
    Np = 201      # 频率点数

    CMC, DMC, f = TWP_far_field(s, h, rw, p, Lz, fmin, fmax, Np)

    # 绘制结果
    plt.figure()
    plt.semilogx(f, 20*np.log10(np.abs(CMC)), 
                 f, 20*np.log10(np.abs(DMC)), 
                 linewidth=2)
    plt.title('End-Fire')
    plt.legend(['CM, analytical', 'DM, analytical'])
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Modal Current (dBA)')
    plt.grid(True)
    plt.show()