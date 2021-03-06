# -*- coding: utf-8 -*-

### code generated by code_generator.py on 2013-11-04 04:42:33.657572 ###

from op import *
import os
os.chdir(os.path.dirname(__file__))

c_il, c_ir, c_el, c_er = 1. + 1.j, 3., 1., 2.
omega = 1.
eps_i, mu_i, beta_i = 1.4, 1.2, 0.
eps_e, mu_e, beta_e = 1.1, 1.15, 0.05

k_i = sqrt(omega**2 * eps_i * mu_i)
k_e = sqrt(omega**2 * eps_e * mu_e)
gamma_ir = k_i / (1 + k_i * beta_i) 
gamma_il = k_i / (1 - k_i * beta_i)
gamma_er = k_e / (1 + k_e * beta_e)
gamma_el = k_e / (1 - k_e * beta_e)
delta = sqrt(mu_i/mu_e)
rho = sqrt(eps_i/eps_e)

Q_er_inf_0 = c_er * sqrt(2/(pi*gamma_er)) * exp(-1j*pi/4)
Q_el_inf_0 = c_el * sqrt(2/(pi*gamma_el)) * exp(-1j*pi/4) 

for d in [[1, 0],]:   # observed direction   
    s_el, s_er = [], []
    for n in [8, 16, 32, 64, 128]:
        tic = dt_now()
        def R(t):
            s = 0.
            for l in arange(1, n):
                s += 1. / l * cos(l * t * pi/n)
            return -2 * pi/n * s - pi/(n**2) * ((-1)**t)

        Q_el_inf, Q_er_inf = 0., 0.

        u = zeros((8*n,), dtype=complex)
        for l in arange(2*n):
            norm = x(l*pi/n)
            d_nu = (x2p(l*pi/n) * x1(l*pi/n) - x1p(l*pi/n) * x2(l*pi/n)) / (xp(l*pi/n) * norm)
            u[4*l + 0] = c_ir * delta * j0(k_i * norm) + c_il * delta * j0(k_i * norm) - c_er * hankel1(0, gamma_er * norm) - c_el * hankel1(0, gamma_el * norm)
            u[4*l + 1] = 1.j * (c_ir * j0(k_i * norm) * rho - c_il * j0(k_i * norm) * rho - c_er * hankel1(0, gamma_er * norm) + c_el * hankel1(0, gamma_el * norm))
            u[4*l + 2] =  - d_nu * (c_ir * delta * j1(k_i * norm) - c_il * delta * j1(k_i * norm) - c_er * hankel1(1, gamma_er * norm) + c_el * hankel1(1, gamma_el * norm))
            u[4*l + 3] =  - 1.j * d_nu * (c_ir * j1(k_i * norm) * rho + c_il * j1(k_i * norm) * rho - c_er * hankel1(1, gamma_er * norm) - c_el * hankel1(1, gamma_el * norm))

        E = zeros((8*n, 8*n), dtype=complex)
        for l in arange(2*n):
            E[4*l + 0, 4*l + 0] =  - ((gamma_er + gamma_el) * rho + 2 * delta * k_i - delta * gamma_er + delta * gamma_el) * 1 / 2
            E[4*l + 0, 4*l + 1] =  - ((gamma_er + gamma_el) * rho + 2 * delta * k_i + delta * gamma_er - delta * gamma_el) * 1 / 2
            E[4*l + 0, 4*l + 2] = 0
            E[4*l + 0, 4*l + 3] = 0
            E[4*l + 1, 4*l + 0] = ((2 * 1.j * k_i - 1.j * gamma_er + 1.j * gamma_el) * rho + 1.j * delta * gamma_er + 1.j * delta * gamma_el) * 1 / 2
            E[4*l + 1, 4*l + 1] =  - ((2 * 1.j * k_i + 1.j * gamma_er - 1.j * gamma_el) * rho + 1.j * delta * gamma_er + 1.j * delta * gamma_el) * 1 / 2
            E[4*l + 1, 4*l + 2] = 0
            E[4*l + 1, 4*l + 3] = 0
            E[4*l + 2, 4*l + 0] = 0
            E[4*l + 2, 4*l + 1] = 0
            E[4*l + 2, 4*l + 2] =  - (k_i + delta * gamma_el) * 1 / (2 * gamma_el * k_i)
            E[4*l + 2, 4*l + 3] = (k_i + delta * gamma_er) * 1 / (2 * gamma_er * k_i)
            E[4*l + 3, 4*l + 0] = 0
            E[4*l + 3, 4*l + 1] = 0
            E[4*l + 3, 4*l + 2] = (1.j * gamma_el * rho + 1.j * k_i) * 1 / (2 * gamma_el * k_i)
            E[4*l + 3, 4*l + 3] = (1.j * gamma_er * rho + 1.j * k_i) * 1 / (2 * gamma_er * k_i)

        A = zeros((8*n, 8*n), dtype=complex)
        for l in arange(2*n):
            for m in arange(2*n):
                A[4*l + 0, 4*m + 0] =  - (R(l - m) * L1(pi*l/n, pi*m/n, gamma_er) + pi/n * L2(pi*l/n, pi*m/n, gamma_er)) * (gamma_er * rho - delta * gamma_er) / 2 - (R(l - m) * L1(pi*l/n, pi*m/n, gamma_el) + pi/n * L2(pi*l/n, pi*m/n, gamma_el)) * (gamma_el * rho + delta * gamma_el) / 2 + delta * k_i * (R(l - m) * L1(pi*l/n, pi*m/n, k_i) + pi/n * L2(pi*l/n, pi*m/n, k_i))
                A[4*l + 0, 4*m + 1] =  - (R(l - m) * L1(pi*l/n, pi*m/n, gamma_er) + pi/n * L2(pi*l/n, pi*m/n, gamma_er)) * (gamma_er * rho + delta * gamma_er) / 2 - (R(l - m) * L1(pi*l/n, pi*m/n, gamma_el) + pi/n * L2(pi*l/n, pi*m/n, gamma_el)) * (gamma_el * rho - delta * gamma_el) / 2 + delta * k_i * (R(l - m) * L1(pi*l/n, pi*m/n, k_i) + pi/n * L2(pi*l/n, pi*m/n, k_i))
                A[4*l + 0, 4*m + 2] = delta * (R(l - m) * M1(pi*l/n, pi*m/n, k_i) + pi/n * M2(pi*l/n, pi*m/n, k_i)) / 2 - (R(l - m) * M1(pi*l/n, pi*m/n, gamma_el) + pi/n * M2(pi*l/n, pi*m/n, gamma_el)) / 2
                A[4*l + 0, 4*m + 3] = delta * (R(l - m) * M1(pi*l/n, pi*m/n, k_i) + pi/n * M2(pi*l/n, pi*m/n, k_i)) / 2 - (R(l - m) * M1(pi*l/n, pi*m/n, gamma_er) + pi/n * M2(pi*l/n, pi*m/n, gamma_er)) / 2
                A[4*l + 1, 4*m + 0] =  - (R(l - m) * L1(pi*l/n, pi*m/n, gamma_er) + pi/n * L2(pi*l/n, pi*m/n, gamma_er)) * (1.j * gamma_er * rho - 1.j * delta * gamma_er) / 2 + (R(l - m) * L1(pi*l/n, pi*m/n, gamma_el) + pi/n * L2(pi*l/n, pi*m/n, gamma_el)) * (1.j * gamma_el * rho + 1.j * delta * gamma_el) / 2 - 1.j * k_i * (R(l - m) * L1(pi*l/n, pi*m/n, k_i) + pi/n * L2(pi*l/n, pi*m/n, k_i)) * rho
                A[4*l + 1, 4*m + 1] =  - (R(l - m) * L1(pi*l/n, pi*m/n, gamma_er) + pi/n * L2(pi*l/n, pi*m/n, gamma_er)) * (1.j * gamma_er * rho + 1.j * delta * gamma_er) / 2 + (R(l - m) * L1(pi*l/n, pi*m/n, gamma_el) + pi/n * L2(pi*l/n, pi*m/n, gamma_el)) * (1.j * gamma_el * rho - 1.j * delta * gamma_el) / 2 + 1.j * k_i * (R(l - m) * L1(pi*l/n, pi*m/n, k_i) + pi/n * L2(pi*l/n, pi*m/n, k_i)) * rho
                A[4*l + 1, 4*m + 2] = 1.j * (R(l - m) * M1(pi*l/n, pi*m/n, gamma_el) + pi/n * M2(pi*l/n, pi*m/n, gamma_el)) / 2 - 1.j * rho * (R(l - m) * M1(pi*l/n, pi*m/n, k_i) + pi/n * M2(pi*l/n, pi*m/n, k_i)) / 2
                A[4*l + 1, 4*m + 3] = 1.j * rho * (R(l - m) * M1(pi*l/n, pi*m/n, k_i) + pi/n * M2(pi*l/n, pi*m/n, k_i)) / 2 - 1.j * (R(l - m) * M1(pi*l/n, pi*m/n, gamma_er) + pi/n * M2(pi*l/n, pi*m/n, gamma_er)) / 2
                A[4*l + 2, 4*m + 0] =  - delta * (R(l - m) * N1(pi*l/n, pi*m/n, k_i) + pi/n * N2(pi*l/n, pi*m/n, k_i)) - (rho - delta) * (R(l - m) * N1(pi*l/n, pi*m/n, gamma_er) + pi/n * N2(pi*l/n, pi*m/n, gamma_er)) / 2 + (rho + delta) * (R(l - m) * N1(pi*l/n, pi*m/n, gamma_el) + pi/n * N2(pi*l/n, pi*m/n, gamma_el)) / 2
                A[4*l + 2, 4*m + 1] = delta * (R(l - m) * N1(pi*l/n, pi*m/n, k_i) + pi/n * N2(pi*l/n, pi*m/n, k_i)) - (rho + delta) * (R(l - m) * N1(pi*l/n, pi*m/n, gamma_er) + pi/n * N2(pi*l/n, pi*m/n, gamma_er)) / 2 + (rho - delta) * (R(l - m) * N1(pi*l/n, pi*m/n, gamma_el) + pi/n * N2(pi*l/n, pi*m/n, gamma_el)) / 2
                A[4*l + 2, 4*m + 2] = (R(l - m) * Ls1(pi*l/n, pi*m/n, gamma_el) + pi/n * Ls2(pi*l/n, pi*m/n, gamma_el)) / (2 * gamma_el) - delta * (R(l - m) * Ls1(pi*l/n, pi*m/n, k_i) + pi/n * Ls2(pi*l/n, pi*m/n, k_i)) / (2 * k_i)
                A[4*l + 2, 4*m + 3] = delta * (R(l - m) * Ls1(pi*l/n, pi*m/n, k_i) + pi/n * Ls2(pi*l/n, pi*m/n, k_i)) / (2 * k_i) - (R(l - m) * Ls1(pi*l/n, pi*m/n, gamma_er) + pi/n * Ls2(pi*l/n, pi*m/n, gamma_er)) / (2 * gamma_er)
                A[4*l + 3, 4*m + 0] = 1.j * rho * (R(l - m) * N1(pi*l/n, pi*m/n, k_i) + pi/n * N2(pi*l/n, pi*m/n, k_i)) - (1.j * rho - 1.j * delta) * (R(l - m) * N1(pi*l/n, pi*m/n, gamma_er) + pi/n * N2(pi*l/n, pi*m/n, gamma_er)) / 2 - (1.j * rho + 1.j * delta) * (R(l - m) * N1(pi*l/n, pi*m/n, gamma_el) + pi/n * N2(pi*l/n, pi*m/n, gamma_el)) / 2
                A[4*l + 3, 4*m + 1] = 1.j * rho * (R(l - m) * N1(pi*l/n, pi*m/n, k_i) + pi/n * N2(pi*l/n, pi*m/n, k_i)) - (1.j * rho + 1.j * delta) * (R(l - m) * N1(pi*l/n, pi*m/n, gamma_er) + pi/n * N2(pi*l/n, pi*m/n, gamma_er)) / 2 - (1.j * rho - 1.j * delta) * (R(l - m) * N1(pi*l/n, pi*m/n, gamma_el) + pi/n * N2(pi*l/n, pi*m/n, gamma_el)) / 2
                A[4*l + 3, 4*m + 2] = 1.j * (R(l - m) * Ls1(pi*l/n, pi*m/n, k_i) + pi/n * Ls2(pi*l/n, pi*m/n, k_i)) * rho / (2 * k_i) - 1.j * (R(l - m) * Ls1(pi*l/n, pi*m/n, gamma_el) + pi/n * Ls2(pi*l/n, pi*m/n, gamma_el)) / (2 * gamma_el)
                A[4*l + 3, 4*m + 3] = 1.j * (R(l - m) * Ls1(pi*l/n, pi*m/n, k_i) + pi/n * Ls2(pi*l/n, pi*m/n, k_i)) * rho / (2 * k_i) - 1.j * (R(l - m) * Ls1(pi*l/n, pi*m/n, gamma_er) + pi/n * Ls2(pi*l/n, pi*m/n, gamma_er)) / (2 * gamma_er)

        z = linalg.solve(E + A, u)
        
        for l in arange(2*n):
            Q_er_inf += (z[4*l+3] * (1.j * xp(l*pi/n)) + (gamma_er * (d[0] * x2p(l*pi/n) - d[1] * x1p(l*pi/n))) * (gamma_er * z[4*l+1] * (rho + delta) + gamma_er * z[4*l] * (rho - delta))) * exp(-1.j * gamma_er * (d[0] * x1(l*pi/n) + d[1] * x2(l*pi/n)))
            Q_el_inf += (z[4*l+2] * (1.j * xp(l*pi/n)) + (gamma_el * (d[0] * x2p(l*pi/n) - d[1] * x1p(l*pi/n))) * (gamma_el * z[4*l] * (rho + delta) + gamma_el * z[4*l+1] * (rho - delta))) * exp(-1.j * gamma_el * (d[0] * x1(l*pi/n) + d[1] * x2(l*pi/n)))
        Q_er_inf = exp(-1j*pi/4) / sqrt(8*pi*gamma_er) * pi/n * Q_er_inf
        Q_el_inf = exp(-1j*pi/4) / sqrt(8*pi*gamma_el) * pi/n * Q_el_inf
        
        print Q_el_inf, Q_el_inf_0, Q_er_inf, Q_er_inf_0, 'running time: ' + lapse(dt_now() - tic)
        s_el.append([str(s) for s in [n, Q_el_inf.real, Q_el_inf.imag, abs(Q_el_inf-Q_el_inf_0)/abs(Q_el_inf_0)]])
        s_er.append([str(s) for s in [n, Q_er_inf.real, Q_er_inf.imag, abs(Q_er_inf-Q_er_inf_0)/abs(Q_er_inf_0)]])

    s1 = make_table(name(__file__)[:-5].replace("_", "--") + ", $\omega=" + str(omega) + "$", (r"\\ " + "\n").join([" & ".join(s) for s in s_el]) + (r"\\ " + "\n"), str(Q_el_inf_0.real), str(Q_el_inf_0.imag), 'l')
    s2 = make_table(name(__file__)[:-5].replace("_", "--") + ", $\omega=" + str(omega) + "$", (r"\\ " + "\n").join([" & ".join(s) for s in s_er]) + (r"\\ " + "\n"), str(Q_er_inf_0.real), str(Q_er_inf_0.imag), 'r')

    open("data/em_chiral_achiral.data", "w").write(s1 + '\n' + s2)
