# -*- coding: utf-8 -*-

### code generated by code_generator.py on 2013-11-06 19:19:52.305476 ###

from op import *
import os
os.chdir(os.path.dirname(__file__))

c_il, c_ir, c_el, c_er = 1. + 1.j, 3., 1., 2.
omega = 1.
eps_i, mu_i, beta_i = 1.4, 1.2, 0.1
eps_e, mu_e, beta_e = 1., 1., 0.

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
            u[4*l + 0] = 2 * (delta * (c_ir * j0(gamma_ir * norm) + c_il * j0(gamma_il * norm)) / 2 - (c_er * hankel1(0, k_e * norm) + c_el * hankel1(0, k_e * norm)) / 2)
            u[4*l + 1] = 2 * (1.j * (c_ir * j0(gamma_ir * norm) - c_il * j0(gamma_il * norm)) * rho / 2 - 1.j * (c_er * hankel1(0, k_e * norm) - c_el * hankel1(0, k_e * norm)) / 2)
            u[4*l + 2] = 2 * (delta * (c_il * d_nu * j1(gamma_il * norm) - c_ir * d_nu * j1(gamma_ir * norm)) / 2 - (c_el * d_nu * hankel1(1, k_e * norm) - c_er * d_nu * hankel1(1, k_e * norm)) / 2)
            u[4*l + 3] = 2 * (1.j * ( - c_ir * d_nu * j1(gamma_ir * norm) - c_il * d_nu * j1(gamma_il * norm)) * rho / 2 - 1.j * ( - c_er * d_nu * hankel1(1, k_e * norm) - c_el * d_nu * hankel1(1, k_e * norm)) / 2)

        E = zeros((8*n, 8*n), dtype=complex)
        for l in arange(2*n):
            E[4*l + 0, 4*l + 0] = ( - k_e * rho - delta * gamma_il) * 1
            E[4*l + 0, 4*l + 1] = ( - k_e * rho - delta * gamma_ir) * 1
            E[4*l + 0, 4*l + 2] = 0
            E[4*l + 0, 4*l + 3] = 0
            E[4*l + 1, 4*l + 0] = (1.j * gamma_il * rho + 1.j * delta * k_e) * 1
            E[4*l + 1, 4*l + 1] = ( - 1.j * gamma_ir * rho - 1.j * delta * k_e) * 1
            E[4*l + 1, 4*l + 2] = 0
            E[4*l + 1, 4*l + 3] = 0
            E[4*l + 2, 4*l + 0] = 0
            E[4*l + 2, 4*l + 1] = 0
            E[4*l + 2, 4*l + 2] =  - (delta * k_e + gamma_il) * 1 / (2 * gamma_il * k_e)
            E[4*l + 2, 4*l + 3] = (delta * k_e + gamma_ir) * 1 / (2 * gamma_ir * k_e)
            E[4*l + 3, 4*l + 0] = 0
            E[4*l + 3, 4*l + 1] = 0
            E[4*l + 3, 4*l + 2] = (1.j * k_e * rho + 1.j * gamma_il) * 1 / (2 * gamma_il * k_e)
            E[4*l + 3, 4*l + 3] = (1.j * k_e * rho + 1.j * gamma_ir) * 1 / (2 * gamma_ir * k_e)

        A = zeros((8*n, 8*n), dtype=complex)
        for l in arange(2*n):
            for m in arange(2*n):
                A[4*l + 0, 4*m + 0] = delta * gamma_il * (R(l - m) * L1(pi*l/n, pi*m/n, gamma_il) + pi/n * L2(pi*l/n, pi*m/n, gamma_il)) - k_e * (R(l - m) * L1(pi*l/n, pi*m/n, k_e) + pi/n * L2(pi*l/n, pi*m/n, k_e)) * rho
                A[4*l + 0, 4*m + 1] = delta * gamma_ir * (R(l - m) * L1(pi*l/n, pi*m/n, gamma_ir) + pi/n * L2(pi*l/n, pi*m/n, gamma_ir)) - k_e * (R(l - m) * L1(pi*l/n, pi*m/n, k_e) + pi/n * L2(pi*l/n, pi*m/n, k_e)) * rho
                A[4*l + 0, 4*m + 2] = delta * (R(l - m) * M1(pi*l/n, pi*m/n, gamma_il) + pi/n * M2(pi*l/n, pi*m/n, gamma_il)) / 2 - (R(l - m) * M1(pi*l/n, pi*m/n, k_e) + pi/n * M2(pi*l/n, pi*m/n, k_e)) / 2
                A[4*l + 0, 4*m + 3] = delta * (R(l - m) * M1(pi*l/n, pi*m/n, gamma_ir) + pi/n * M2(pi*l/n, pi*m/n, gamma_ir)) / 2 - (R(l - m) * M1(pi*l/n, pi*m/n, k_e) + pi/n * M2(pi*l/n, pi*m/n, k_e)) / 2
                A[4*l + 1, 4*m + 0] = 1.j * delta * k_e * (R(l - m) * L1(pi*l/n, pi*m/n, k_e) + pi/n * L2(pi*l/n, pi*m/n, k_e)) - 1.j * gamma_il * (R(l - m) * L1(pi*l/n, pi*m/n, gamma_il) + pi/n * L2(pi*l/n, pi*m/n, gamma_il)) * rho
                A[4*l + 1, 4*m + 1] = 1.j * gamma_ir * (R(l - m) * L1(pi*l/n, pi*m/n, gamma_ir) + pi/n * L2(pi*l/n, pi*m/n, gamma_ir)) * rho - 1.j * delta * k_e * (R(l - m) * L1(pi*l/n, pi*m/n, k_e) + pi/n * L2(pi*l/n, pi*m/n, k_e))
                A[4*l + 1, 4*m + 2] = 1.j * (R(l - m) * M1(pi*l/n, pi*m/n, k_e) + pi/n * M2(pi*l/n, pi*m/n, k_e)) / 2 - 1.j * rho * (R(l - m) * M1(pi*l/n, pi*m/n, gamma_il) + pi/n * M2(pi*l/n, pi*m/n, gamma_il)) / 2
                A[4*l + 1, 4*m + 3] = 1.j * rho * (R(l - m) * M1(pi*l/n, pi*m/n, gamma_ir) + pi/n * M2(pi*l/n, pi*m/n, gamma_ir)) / 2 - 1.j * (R(l - m) * M1(pi*l/n, pi*m/n, k_e) + pi/n * M2(pi*l/n, pi*m/n, k_e)) / 2
                A[4*l + 2, 4*m + 0] = delta * (R(l - m) * N1(pi*l/n, pi*m/n, k_e) + pi/n * N2(pi*l/n, pi*m/n, k_e)) - delta * (R(l - m) * N1(pi*l/n, pi*m/n, gamma_il) + pi/n * N2(pi*l/n, pi*m/n, gamma_il))
                A[4*l + 2, 4*m + 1] = delta * (R(l - m) * N1(pi*l/n, pi*m/n, gamma_ir) + pi/n * N2(pi*l/n, pi*m/n, gamma_ir)) - delta * (R(l - m) * N1(pi*l/n, pi*m/n, k_e) + pi/n * N2(pi*l/n, pi*m/n, k_e))
                A[4*l + 2, 4*m + 2] = (R(l - m) * Ls1(pi*l/n, pi*m/n, k_e) + pi/n * Ls2(pi*l/n, pi*m/n, k_e)) / (2 * k_e) - delta * (R(l - m) * Ls1(pi*l/n, pi*m/n, gamma_il) + pi/n * Ls2(pi*l/n, pi*m/n, gamma_il)) / (2 * gamma_il)
                A[4*l + 2, 4*m + 3] = delta * (R(l - m) * Ls1(pi*l/n, pi*m/n, gamma_ir) + pi/n * Ls2(pi*l/n, pi*m/n, gamma_ir)) / (2 * gamma_ir) - (R(l - m) * Ls1(pi*l/n, pi*m/n, k_e) + pi/n * Ls2(pi*l/n, pi*m/n, k_e)) / (2 * k_e)
                A[4*l + 3, 4*m + 0] = 1.j * rho * (R(l - m) * N1(pi*l/n, pi*m/n, gamma_il) + pi/n * N2(pi*l/n, pi*m/n, gamma_il)) - 1.j * rho * (R(l - m) * N1(pi*l/n, pi*m/n, k_e) + pi/n * N2(pi*l/n, pi*m/n, k_e))
                A[4*l + 3, 4*m + 1] = 1.j * rho * (R(l - m) * N1(pi*l/n, pi*m/n, gamma_ir) + pi/n * N2(pi*l/n, pi*m/n, gamma_ir)) - 1.j * rho * (R(l - m) * N1(pi*l/n, pi*m/n, k_e) + pi/n * N2(pi*l/n, pi*m/n, k_e))
                A[4*l + 3, 4*m + 2] = 1.j * (R(l - m) * Ls1(pi*l/n, pi*m/n, gamma_il) + pi/n * Ls2(pi*l/n, pi*m/n, gamma_il)) * rho / (2 * gamma_il) - 1.j * (R(l - m) * Ls1(pi*l/n, pi*m/n, k_e) + pi/n * Ls2(pi*l/n, pi*m/n, k_e)) / (2 * k_e)
                A[4*l + 3, 4*m + 3] = 1.j * (R(l - m) * Ls1(pi*l/n, pi*m/n, gamma_ir) + pi/n * Ls2(pi*l/n, pi*m/n, gamma_ir)) * rho / (2 * gamma_ir) - 1.j * (R(l - m) * Ls1(pi*l/n, pi*m/n, k_e) + pi/n * Ls2(pi*l/n, pi*m/n, k_e)) / (2 * k_e)

        z = linalg.solve(E + A, u)
        
        for l in arange(2*n):
            Q_er_inf += (z[4*l+3] * (1.j * xp(l*pi/n)) + (k_e * (d[0] * x2p(l*pi/n) - d[1] * x1p(l*pi/n))) * (z[4*l+1] * k_e * (rho + delta) + z[4*l] * k_e * (rho - delta))) * exp(-1.j * gamma_er * (d[0] * x1(l*pi/n) + d[1] * x2(l*pi/n)))
            Q_el_inf += (z[4*l+2] * (1.j * xp(l*pi/n)) + (k_e * (d[0] * x2p(l*pi/n) - d[1] * x1p(l*pi/n))) * (z[4*l] * k_e * (rho + delta) + z[4*l+1] * k_e * (rho - delta))) * exp(-1.j * gamma_el * (d[0] * x1(l*pi/n) + d[1] * x2(l*pi/n)))
        Q_er_inf = exp(-1j*pi/4) / sqrt(8*pi*gamma_er) * pi/n * Q_er_inf
        Q_el_inf = exp(-1j*pi/4) / sqrt(8*pi*gamma_el) * pi/n * Q_el_inf
        
        print Q_el_inf, Q_el_inf_0, Q_er_inf, Q_er_inf_0, 'running time: ' + lapse(dt_now() - tic)
        s_el.append([str(s) for s in [n, Q_el_inf.real, Q_el_inf.imag, abs(Q_el_inf-Q_el_inf_0)/abs(Q_el_inf_0)]])
        s_er.append([str(s) for s in [n, Q_er_inf.real, Q_er_inf.imag, abs(Q_er_inf-Q_er_inf_0)/abs(Q_er_inf_0)]])

    s1 = make_table(name(__file__)[:-5].replace("_", "--") + ", $\omega=" + str(omega) + "$", (r"\\ " + "\n").join([" & ".join(s) for s in s_el]) + (r"\\ " + "\n"), str(Q_el_inf_0.real), str(Q_el_inf_0.imag), 'l')
    s2 = make_table(name(__file__)[:-5].replace("_", "--") + ", $\omega=" + str(omega) + "$", (r"\\ " + "\n").join([" & ".join(s) for s in s_er]) + (r"\\ " + "\n"), str(Q_er_inf_0.real), str(Q_er_inf_0.imag), 'r')

    open("data/em_achiral_chiral.data", "w").write(s1 + '\n' + s2)
