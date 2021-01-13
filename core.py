import numpy as np
import cmath

#constants SGS
e = 4.8 * 10 ** (-10)
c = 2.998 * 10 ** (10)
m_e = 9.1 * 10 ** (-28)

#Users constants
N = 10 ** 17 * 10 ** 22 #cm^-3
M = 1 * 9.1 * 10 ** (-28) #mass of charge carriers in mass of free electrons
eps_inf = 10 #(1 - 100)
W_LO = 300 #freq. for longitudinal phonon, cm^-1
W_TO = 270 #freq. for longitudinal phonon, cm^-1
G_1 = 5 #phonon attenuation, cm^-1
G_0 = 10 #plasmon attenuation
d = 10 ** (-5) #film thinkness, 0 - 10^-3 cm^-1

def plasmon_freq(N, effective_mass, eps_infinum):
  return ( (4 * np.pi * N)/(effective_mass * eps_infinum) ) ** (1/2) * e / c

def eps_total(_w, _eps_infinum = eps_inf, _w_LO = W_LO, _w_TO = W_TO, _g_1 = G_1, _Omega_P = 1, _g_0 = G_0):
  #print(_w, (_w_LO ** 2 - _w_TO ** 2) / (_w_TO**2 - _w**2 - 1j*_w*_g_1), "-", _Omega_P / (_w**2 + 1j*_w*_g_0))
  return _eps_infinum * (1 + (_w_LO ** 2 - _w_TO ** 2) / (_w_TO**2 - _w**2 - 1j*_w*_g_1) - _Omega_P ** 2 / (_w**2 + 1j*_w*_g_0))

def N_w(w):
  return (eps_total(_w = w)) ** (1 / 2)

def alpha_W(w):
  return 4 * np.pi * np.imag(eps_total(_w = w)) * w

def r_w(w):
  return (1 - N_w(w)) / (1 + N_w(w))

def phi_w(w):
  return cmath.phase(r_w(w))

def R_w(w):
  return r_w(w) * complex(r_w(w)).conjugate()

def T_w(w):
  return ( (1 - R_w(w)) ** 2 * np.exp(-alpha_W(w) * d) ) / ( 1 - R_w(w) ** 2 * np.exp(-2 * alpha_W(w) * d) )

def A_w(w):
  return -np.log(T_w(w))

w = [i for i in range(1, 1000)]
Omega_P = plasmon_freq(N, 1, eps_inf)
Re_eps_total_list = [np.real(eps_total(_w = i, _Omega_P=Omega_P)) for i in w]
Im_eps_total_list = [np.imag(eps_total(_w = i, _Omega_P=Omega_P)) for i in w]
N_w_list = [np.real(N_w(i)) for i in w]
K_w_list = [np.imag(N_w(i)) for i in w]
R_w_list = [R_w(i) for i in w]
phi_w_list = [phi_w(i) for i in w]
alpha_w_list = [alpha_W(i) for i in w]
T_w_list = [T_w(i) for i in w]
A_w_list = [A_w(i) for i in w]

def update():
    global N
    print("N =", N)

    global Re_eps_total_list, Im_eps_total_list, N_w_list, K_w_list, R_w_list, phi_w_list, alpha_w_list, T_w_list, A_w_list
    Omega_P = plasmon_freq(N, 1, eps_inf)
    Re_eps_total_list = [np.real(eps_total(_w=i, _Omega_P=Omega_P)) for i in w]
    Im_eps_total_list = [np.imag(eps_total(_w=i, _Omega_P=Omega_P)) for i in w]
    N_w_list = [np.real(N_w(i)) for i in w]
    K_w_list = [np.imag(N_w(i)) for i in w]
    R_w_list = [R_w(i) for i in w]
    phi_w_list = [phi_w(i) for i in w]
    alpha_w_list = [alpha_W(i) for i in w]
    T_w_list = [T_w(i) for i in w]
    A_w_list = [A_w(i) for i in w]


class user_constant:
    def __init__(self):
        N = 10 ** 17 * 10 ** 22  # cm^-3
        M = 1 * 9.1 * 10 ** (-28)  # mass of charge carriers in mass of free electrons
        eps_inf = 10  # (1 - 100)
        W_LO = 300  # freq. for longitudinal phonon, cm^-1
        W_TO = 270  # freq. for longitudinal phonon, cm^-1
        G_1 = 5  # phonon attenuation, cm^-1
        G_0 = 10  # plasmon attenuation
        d = 10 ** (-5)  # film thinkness, 0 - 10^-3 cm^-1

