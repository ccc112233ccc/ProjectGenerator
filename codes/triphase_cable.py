import numpy as np
from scipy.constants import mu_0, epsilon_0, c
from scipy.linalg import expm
from scipy.special import ive, kve
from scipy.integrate import quad
from scipy.linalg import block_diag
import matplotlib.pyplot as plt

# Scaled Bessel functions (robust implementations)
def besseli_scaled(nu, x):
    return ive(nu, x)
def besselk_scaled(nu, x):
    return kve(nu, x)
# Integrand for Zsh integral calculation
def integrand_fun(phi, alpha1, phi1, alpha2, phi2):
    PI_1 = (1 - alpha1**2) / (1 + alpha1**2 - 2*alpha1*np.cos(phi - phi1))
    PI_2 = (1 - alpha2**2) / (1 + alpha2**2 - 2*alpha2*np.cos(phi - phi2))
    return PI_1 * PI_2
# Complete Zsh integral calculation
def calc_Zsh_in_integral(pos, r_cond, rsh, beta, sigma_shield, Zsh_in_base):
    N = pos.shape[0]
    Zsh_in = np.zeros((N, N), dtype=complex)
    alpha = np.zeros(N, dtype=complex)

    for idx in range(N):
        Zi = pos[idx, 0] + 1j * pos[idx, 1]
        DELTA = (r_cond ** 2 - Zi ** 2 - rsh ** 2) ** 2 - 4 * (Zi * rsh) ** 2
        alpha[idx] = 0 if np.abs(Zi) == 0 else \
            (-(r_cond ** 2 - Zi ** 2 - rsh ** 2) - np.sqrt(DELTA)) / (2 * Zi * rsh)

    for i in range(N):
        Zsh_in[i, i] = Zsh_in_base * (1 + alpha[i] ** 2) / (1 - alpha[i] ** 2)
        for j in range(N):
            if i != j:
                phi_i = np.angle(pos[i, 0] + 1j * pos[i, 1])
                phi_j = np.angle(pos[j, 0] + 1j * pos[j, 1])

                integrand_real = lambda phi: np.real(integrand_fun(phi, alpha[i], phi_i, alpha[j], phi_j))
                integrand_imag = lambda phi: np.imag(integrand_fun(phi, alpha[i], phi_i, alpha[j], phi_j))

                try:
                    integral_real, _ = quad(integrand_real, 0, 2*np.pi, limit=500, epsabs=1e-6, epsrel=1e-4)
                    integral_imag, _ = quad(integrand_imag, 0, 2*np.pi, limit=500, epsabs=1e-6, epsrel=1e-4)
                except:
                    integral_real, integral_imag = 0, 0

                integral_result = integral_real + 1j * integral_imag

                Zsh_in[i, j] = Zsh_in_base * integral_result

    return Zsh_in
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

def custom_expm(A):
    from scipy.linalg import norm

    if A.shape[0] != A.shape[1]:
        raise ValueError("Matrix must be square")

    ident = np.eye(A.shape[0], dtype=complex)
    normA = norm(A, ord=np.inf)

    # Pade coefficients for m = 13
    b = [64764752532480000, 32382376266240000, 7771770303897600,
         1187353796428800, 129060195264000, 10559470521600,
         670442572800, 33522128640, 1323241920, 40840800,
         960960, 16380, 182, 1]

    # Scaling factor
    maxnorm = 5.371920351148152
    s = max(0, int(np.ceil(np.log2(normA / maxnorm))))
    A_scaled = A / (2**s)

    A2 = A_scaled @ A_scaled
    A4 = A2 @ A2
    A6 = A2 @ A4

    U = A_scaled @ (A6 @ (b[13]*A6 + b[11]*A4 + b[9]*A2) + b[7]*A6 + b[5]*A4 + b[3]*A2 + b[1]*ident)
    V = A6 @ (b[12]*A6 + b[10]*A4 + b[8]*A2) + b[6]*A6 + b[4]*A4 + b[2]*A2 + b[0]*ident

    P = V + U
    Q = V - U
    F = np.linalg.solve(Q, P)

    for _ in range(s):
        F = F @ F

    return F
# Complete triphase s-parameter calculation
def calc_triphase_sparams(r_cond, rsh, Rsh, length, pos,
                          sigma_cond, sigma_shield, mu, epsr, tan_delta, freq):
    Nf = len(freq)
    N = pos.shape[0]
    Z0 = 50
    c0 = c

    d = np.linalg.norm(pos, axis=1)
    L_static = np.zeros((N, N), dtype=np.float64)

    for i in range(N):
        for j in range(N):
            if i == j:
                L_static[i, i] = mu / (2 * np.pi) * np.log((rsh ** 2 - d[i] ** 2) / (rsh * r_cond))
            else:
                dij = np.linalg.norm(pos[i] - pos[j])
                theta_i = np.angle(pos[i, 0] + 1j * pos[i, 1])
                theta_j = np.angle(pos[j, 0] + 1j * pos[j, 1])
                theta = theta_i - theta_j
                num = (d[i] * d[j]) ** 2 + rsh ** 4 - 2 * d[i] * d[j] * rsh ** 2 * np.cos(theta)
                den = (d[i] * d[j]) ** 2 + d[j] ** 4 - 2 * d[i] * d[j] ** 3 * np.cos(theta)
                L_static[i, j] = mu / (2 * np.pi) * np.log((d[j] / rsh) * np.sqrt(num / den))

    C_static = (c0 ** -2) * np.linalg.inv(L_static) * epsr * (1 - 1j * tan_delta)
    # L_nH = np.array([
    #     [247.22087, 54.46643, 54.46553],
    #     [54.46643, 247.22654, 54.46646],
    #     [54.46553, 54.46646, 247.22106]
    # ])
    #
    # L_static = L_nH * 1e-9
    # C_static = (c0 ** -2) * np.linalg.inv(L_static) * epsr * (1 - 1j * tan_delta)

    s_params = np.zeros((2 * N, 2 * N, Nf), dtype=complex)
    ChainA = np.zeros((2 * N, 2 * N, Nf), dtype=complex)

    for idx, f in enumerate(freq):
        w = 2 * np.pi * f
        delta = 1 / np.sqrt(np.pi * f * mu_0 * sigma_cond)
        beta = (1 + 1j) / delta

        Zcond = np.zeros((N, N), dtype=complex)

        for i in range(N):
            Zac = (beta / (2 * np.pi * sigma_cond * r_cond)) * besseli_scaled(0, beta * r_cond) / besseli_scaled(1, beta * r_cond)
            Zcond[i, i] = Zac

        Zsh_in_base = beta / (2 * np.pi * sigma_shield * rsh)
        Zsh_in = calc_Zsh_in_integral(pos, r_cond, rsh, beta, sigma_shield, Zsh_in_base)

        Z = Zsh_in + Zcond + 1j * w * L_static
        Y = 1j * w * C_static

        A_matrix = -np.block([[np.zeros((N, N)), Z], [Y, np.zeros((N, N))]])
        chaina = custom_expm(-A_matrix * length)

        ChainA[:, :, idx] = chaina
    s_params = abcd2s(ChainA, Z0)
    SDD, SDC, SCD, SCC = s2smm(s_params, 2)
    S_mixed = np.zeros((6, 6, Nf), dtype=complex)
    S_mixed[0:3, 0:3, :] = SDD
    S_mixed[0:3, 3:6, :] = SDC
    S_mixed[3:6, 0:3, :] = SCD
    S_mixed[3:6, 3:6, :] = SCC
    freq_out = freq
    # test_val = [ChainA[0, 0, i] for i in range(len(freq))]
    # plt.plot(freq * 1e-6, np.real(test_val))
    # plt.title("Real part of ChainA[0,0,:]")
    # plt.show()

    return s_params, S_mixed, freq_out


# Example usage
def main():
    freq = np.linspace(1,100e6, 2001)
    pos = np.array([[1, 0], [-0.5, np.sqrt(3) / 2], [-0.5, -np.sqrt(3) / 2]]) * (
                2 * 0.0125 / np.sqrt(3))

    s_params, S_mixed, freq_out = calc_triphase_sparams(
        r_cond=6.5e-3,
        rsh=0.0309,
        Rsh=0.0329,
        length=2,
        pos=pos,
        sigma_cond=5.813e7,
        sigma_shield=3.816e7,
        mu=mu_0,
        epsr=1,
        tan_delta=0,
        freq=freq
    )

    plt.plot(freq_out * 1e-6, 20 * np.log10(np.abs(s_params[0,0, :])))
    plt.xlabel('Frequency (MHz)')
    plt.ylabel('S11 (dB)')
    plt.title('S11 Parameter vs Frequency')
    plt.grid(True)
    plt.show()

if __name__ == '__main__':
    main()
