# -*- coding: utf-8 -*- 
import os, math, datetime
os.chdir(os.path.dirname(__file__))
now = datetime.datetime.now()

code = ur"""# -*- coding: utf-8 -*-

### code generated by code_generator.py on %s ###

from op import *
import os
os.chdir(os.path.dirname(__file__))
%s

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

%s

%s

%s

        z = linalg.solve(E + A, u)
%s
        
        print Q_el_inf, Q_el_inf_0, Q_er_inf, Q_er_inf_0, 'running time: ' + lapse(dt_now() - tic)
        s_el.append([str(s) for s in [n, Q_el_inf.real, Q_el_inf.imag, abs(Q_el_inf-Q_el_inf_0)/abs(Q_el_inf_0)]])
        s_er.append([str(s) for s in [n, Q_er_inf.real, Q_er_inf.imag, abs(Q_er_inf-Q_er_inf_0)/abs(Q_er_inf_0)]])

    s1 = make_table(name(__file__)[:-5].replace("_", "--") + ", $\omega=" + str(omega) + "$", (r"\\ " + "\n").join([" & ".join(s) for s in s_el]) + (r"\\ " + "\n"), str(Q_el_inf_0.real), str(Q_el_inf_0.imag), 'l')
    s2 = make_table(name(__file__)[:-5].replace("_", "--") + ", $\omega=" + str(omega) + "$", (r"\\ " + "\n").join([" & ".join(s) for s in s_er]) + (r"\\ " + "\n"), str(Q_er_inf_0.real), str(Q_er_inf_0.imag), 'r')

    open("data/em_%s.data", "w").write(s1 + '\n' + s2)
""" 

def make_indent(s, spaces=8):
    return '\n'.join([(spaces * ' ' + ss) for ss in s.split('\n')])

for case in ['chiral_conductor', 'achiral_chiral', 'chiral_chiral', 'chiral_achiral', 'achiral_chiral_3d', 'chiral_chiral_3d', 'chiral_achiral_3d',]: #'achiral_chiral_gerlach']
    all_c = [l.strip().replace(';','') for l in open('data/all_c_%s' % case, 'r') if l.strip()]
    all_q = [l.strip().replace(';','') for l in open('data/all_q_%s' % case, 'r') if l.strip()]
    all_e = [l.strip().replace(';','') for l in open('data/all_e_%s' % case, 'r') if l.strip()]
    all_a = [l.strip().replace(';','') for l in open('data/all_a_%s' % case, 'r') if l.strip()]
    if case.find('_3d') == -1:
        all_u = [l.strip().replace(';','') for l in open('data/all_u_%s' % case, 'r') if l.strip()]
    all_eq = [l.strip().replace(';','') for l in open('data/all_eq_%s' % case, 'r') if l.strip()]
    all_bv = [l.strip().replace(';','') for l in open('data/all_bv_%s' % case, 'r') if l.strip()]
    all_det = [l.strip().replace(';','') for l in open('data/all_det_%s' % case, 'r') if l.strip()]
    all_rawc = [l.strip().replace(';','') for l in open('data/all_rawc_%s' % case, 'r') if l.strip()]

    n = int(math.sqrt(len(all_c)))

    def tex(s):
        tex_rules = [
          ("Q_il", r"Q_\text{il}"), 
          ("Q_ir", r"Q_\text{ir}"), 
          ("Q_el", r"Q_\text{el}"), 
          ("Q_er", r"Q_\text{er}"), 
          ("psi1", r"\psi_1"), 
          ("psi2", r"\psi_2"), 
          ("psi3", r"\psi_3"), 
          ("psi4", r"\psi_4"), 
          ("z11", r"\zeta_{11}"), 
          ("z12", r"\zeta_{12}"), 
          ("z13", r"\zeta_{13}"),
          ("z14", r"\zeta_{14}"), 
          ("z21", r"\zeta_{21}"),
          ("z22", r"\zeta_{22}"),
          ("z23", r"\zeta_{23}"),
          ("z24", r"\zeta_{24}"),
          ("z31", r"\zeta_{31}"), 
          ("z32", r"\zeta_{32}"),
          ("z33", r"\zeta_{33}"),
          ("z34", r"\zeta_{34}"),
          ("z41", r"\zeta_{41}"),
          ("z42", r"\zeta_{42}"),
          ("z43", r"\zeta_{43}"),
          ("z44", r"\zeta_{44}"),
          ("K_g_il_i", r"K^{\text{i}}_{\gamma_\text{il}}"),
          ("K_g_ir_i", r"K^{\text{i}}_{\gamma_\text{ir}}"), 
          ("K_g_el_e", r"K^{\text{e}}_{\gamma_\text{el}}"),
          ("K_g_er_e", r"K^{\text{e}}_{\gamma_\text{er}}"), 
          ("S_g_il_i", r"S^{\text{i}}_{\gamma_\text{il}}"), 
          ("S_g_ir_i", r"S^{\text{i}}_{\gamma_\text{ir}}"), 
          ("S_g_el_e", r"S^{\text{e}}_{\gamma_\text{el}}"),
          ("S_g_er_e", r"S^{\text{e}}_{\gamma_\text{er}}"), 

          ("M_g_il_i", r"M^{\text{i}}_{\gamma_\text{il}}"),
          ("M_g_ir_i", r"M^{\text{i}}_{\gamma_\text{ir}}"), 
          ("M_g_el_e", r"M^{\text{e}}_{\gamma_\text{el}}"),
          ("M_g_er_e", r"M^{\text{e}}_{\gamma_\text{er}}"), 
          ("N_g_il_i", r"N^{\text{i}}_{\gamma_\text{il}}"),
          ("N_g_ir_i", r"N^{\text{i}}_{\gamma_\text{ir}}"), 
          ("N_g_el_e", r"N^{\text{e}}_{\gamma_\text{el}}"),
          ("N_g_er_e", r"N^{\text{e}}_{\gamma_\text{er}}"), 
          ("M_i_i", r"M^{\text{i}}_{k_\text{i}}"), 
          ("M_e_e", r"M^{\text{e}}_{k_\text{e}}"),
          ("N_i_i", r"N^{\text{i}}_{k_\text{i}}"), 
          ("N_e_e", r"N^{\text{e}}_{k_\text{e}}"),

          ("K_i_i", r"K^{\text{i}}_{k_\text{i}}"), 
          ("K_e_e", r"K^{\text{e}}_{k_\text{e}}"), 
          ("S_i_i", r"S^{\text{i}}_{k_\text{i}}"), 
          ("S_e_e", r"S^{\text{e}}_{k_\text{e}}"),

          ("N_g_il", r"N_{\gamma_\text{il}}"), 
          ("N_g_ir", r"N_{\gamma_\text{ir}}"),
          ("N_g_el", r"N_{\gamma_\text{el}}"),
          ("N_g_er", r"N_{\gamma_\text{er}}"),

          ("M_g_il", r"M_{\gamma_\text{il}}"), 
          ("M_g_ir", r"M_{\gamma_\text{ir}}"),
          ("M_g_el", r"M_{\gamma_\text{el}}"),
          ("M_g_er", r"M_{\gamma_\text{er}}"),

          ("K_g_il", r"K_{\gamma_\text{il}}"), 
          ("K_g_ir", r"K_{\gamma_\text{ir}}"),
          ("K_g_el", r"K_{\gamma_\text{el}}"),
          ("K_g_er", r"K_{\gamma_\text{er}}"),
          ("Ks_g_il", r"K'_{\gamma_\text{il}}"),
          ("Ks_g_ir", r"K'_{\gamma_\text{ir}}"),
          ("Ks_g_el", r"K'_{\gamma_\text{el}}"),
          ("Ks_g_er", r"K'_{\gamma_\text{er}}"),
          ("S_g_il", r"S_{\gamma_\text{il}}"),
          ("S_g_ir", r"S_{\gamma_\text{ir}}"),
          ("S_g_el", r"S_{\gamma_\text{el}}"),
          ("S_g_er", r"S_{\gamma_\text{er}}"),
          ("T_g_il", r"T_{\gamma_\text{il}}"), 
          ("T_g_ir", r"T_{\gamma_\text{ir}}"),
          ("T_g_el", r"T_{\gamma_\text{el}}"),
          ("T_g_er", r"T_{\gamma_\text{er}}"),
          
          ("N_i", r"N_{k_\text{i}}"),
          ("N_e", r"N_{k_\text{e}}"),
          ("M_i", r"M_{k_\text{i}}"),
          ("M_e", r"M_{k_\text{e}}"),

          ("K_i", r"K_{k_\text{i}}"),
          ("K_e", r"K_{k_\text{e}}"),
          ("Ks_i", r"K'_{k_\text{i}}"),
          ("Ks_e", r"K'_{k_\text{e}}"),
          ("S_i", r"S_{k_\text{i}}"),
          ("S_e", r"S_{k_\text{e}}"),
          ("T_i", r"T_{k_\text{i}}"),
          ("T_e", r"T_{k_\text{e}}"),
          ("beta_e", r"\beta_\text{e}"),
          ("beta_i", r"\beta_\text{i}"),
          ("k_e", r"k_\text{e}"),
          ("k_i", r"k_\text{i}"),
          ("gamma_il", r"\gamma_\text{il}"),
          ("gamma_ir", r"\gamma_\text{ir}"),
          ("gamma_el", r"\gamma_\text{el}"),
          ("gamma_er", r"\gamma_\text{er}"),
          ("rho", r"\rho"),
          ("delta", r"\delta"),
          ("I", r"I"),
          ("%i", r"i"),
          ("mu_e", r"\mu_\text{e}"),
          ("eps_e", r"\varepsilon_\text{e}"),
          ("mu_i", r"\mu_\text{i}"),
          ("eps_i", r"\varepsilon_\text{i}"),
          ("J0_ir", r"J_0(\gamma_\text{ir}|x|)"),
          ("J0_il", r"J_0(\gamma_\text{il}|x|)"),
          ("H0_er", r"H_0^1(\gamma_\text{er}|x|)"),
          ("H0_el", r"H_0^1(\gamma_\text{el}|x|)"),
          ("J1_ir", r"J_1(\gamma_\text{ir}|x|)"),
          ("J1_il", r"J_1(\gamma_\text{il}|x|)"),
          ("H1_er", r"H_1^1(\gamma_\text{er}|x|)"),
          ("H1_el", r"H_1^1(\gamma_\text{el}|x|)"),
          ("d_nu", r"\nu(x)\cdot\frac{x}{|x|}"),
          ("J0_i", r"J_0(k_\text{i}|x|)"),
          ("J1_i", r"J_1(k_\text{i}|x|)"),
          ("H0_e", r"H_0^1(k_\text{e}|x|)"),
          ("H1_e", r"H_1^1(k_\text{e}|x|)"),
          ("c_er", r"c_\text{er}"),
          ("c_el", r"c_\text{el}"),
          ("c_ir", r"c_\text{ir}"),
          ("c_il", r"c_\text{il}"),
          ("*", r" "),
          ("w0", r"w_0"),
          ("w1", r"w_1"),
          ("v0", r"v_0"),
          ("v1", r"v_1"),
        ]

        s1 = s
        for r1, r2 in tex_rules:
            s1 = s1.replace(r1, r2)
        return s1

    def make_tex():
        sl = []
        sl.append('\n% all_rawc')
        for s in all_rawc:
            sl.append(tex(s))
        sl.append('\n% all_c')
        for s in all_c:
            sl.append(tex(s))
        sl.append('\n% all_q')
        for s in all_q:
            sl.append(tex(s))
        sl.append('\n% all_u')
        for s in all_u:
            sl.append(tex(s))
        sl.append('\n% all_eq')
        for s in all_eq:
            sl.append(tex(s))
        sl.append('\n% all_bv')
        for s in all_bv:
            sl.append(tex(s))
        sl.append('\n% all_det')
        for s in all_det:
            sl.append(tex(s))
        return '\n'.join(sl)

    def py(s):
        py_rules = [
        ("+", r" + "),
        ("-", r" - "),
        ("*", r" * "),
        ("/", r" / "),
        ("^", r" ** "),
        ("I", r"1"),
        ("K_g_ir", r"(R(l - m) * L1(pi*l/n, pi*m/n, gamma_ir) + pi/n * L2(pi*l/n, pi*m/n, gamma_ir))"),
        ("K_g_il", r"(R(l - m) * L1(pi*l/n, pi*m/n, gamma_il) + pi/n * L2(pi*l/n, pi*m/n, gamma_il))"),
        ("K_g_er", r"(R(l - m) * L1(pi*l/n, pi*m/n, gamma_er) + pi/n * L2(pi*l/n, pi*m/n, gamma_er))"),
        ("K_g_el", r"(R(l - m) * L1(pi*l/n, pi*m/n, gamma_el) + pi/n * L2(pi*l/n, pi*m/n, gamma_el))"),
        ("Ks_g_ir", r"(R(l - m) * Ls1(pi*l/n, pi*m/n, gamma_ir) + pi/n * Ls2(pi*l/n, pi*m/n, gamma_ir))"),
        ("Ks_g_il", r"(R(l - m) * Ls1(pi*l/n, pi*m/n, gamma_il) + pi/n * Ls2(pi*l/n, pi*m/n, gamma_il))"),
        ("Ks_g_er", r"(R(l - m) * Ls1(pi*l/n, pi*m/n, gamma_er) + pi/n * Ls2(pi*l/n, pi*m/n, gamma_er))"),
        ("Ks_g_el", r"(R(l - m) * Ls1(pi*l/n, pi*m/n, gamma_el) + pi/n * Ls2(pi*l/n, pi*m/n, gamma_el))"),
        ("S_g_ir", r"(R(l - m) * M1(pi*l/n, pi*m/n, gamma_ir) + pi/n * M2(pi*l/n, pi*m/n, gamma_ir))"),
        ("S_g_il", r"(R(l - m) * M1(pi*l/n, pi*m/n, gamma_il) + pi/n * M2(pi*l/n, pi*m/n, gamma_il))"),
        ("S_g_er", r"(R(l - m) * M1(pi*l/n, pi*m/n, gamma_er) + pi/n * M2(pi*l/n, pi*m/n, gamma_er))"),
        ("S_g_el", r"(R(l - m) * M1(pi*l/n, pi*m/n, gamma_el) + pi/n * M2(pi*l/n, pi*m/n, gamma_el))"),
        ("T_g_ir", r"(R(l - m) * N1(pi*l/n, pi*m/n, gamma_ir) + pi/n * N2(pi*l/n, pi*m/n, gamma_ir))"),
        ("T_g_il", r"(R(l - m) * N1(pi*l/n, pi*m/n, gamma_il) + pi/n * N2(pi*l/n, pi*m/n, gamma_il))"),
        ("T_g_er", r"(R(l - m) * N1(pi*l/n, pi*m/n, gamma_er) + pi/n * N2(pi*l/n, pi*m/n, gamma_er))"),
        ("T_g_el", r"(R(l - m) * N1(pi*l/n, pi*m/n, gamma_el) + pi/n * N2(pi*l/n, pi*m/n, gamma_el))"),
        ("K_i", r"(R(l - m) * L1(pi*l/n, pi*m/n, k_i) + pi/n * L2(pi*l/n, pi*m/n, k_i))"),
        ("K_e", r"(R(l - m) * L1(pi*l/n, pi*m/n, k_e) + pi/n * L2(pi*l/n, pi*m/n, k_e))"),
        ("Ks_i", r"(R(l - m) * Ls1(pi*l/n, pi*m/n, k_i) + pi/n * Ls2(pi*l/n, pi*m/n, k_i))"),
        ("Ks_e", r"(R(l - m) * Ls1(pi*l/n, pi*m/n, k_e) + pi/n * Ls2(pi*l/n, pi*m/n, k_e))"),
        ("S_i", r"(R(l - m) * M1(pi*l/n, pi*m/n, k_i) + pi/n * M2(pi*l/n, pi*m/n, k_i))"),
        ("S_e", r"(R(l - m) * M1(pi*l/n, pi*m/n, k_e) + pi/n * M2(pi*l/n, pi*m/n, k_e))"),
        ("T_i", r"(R(l - m) * N1(pi*l/n, pi*m/n, k_i) + pi/n * N2(pi*l/n, pi*m/n, k_i))"),
        ("T_e", r"(R(l - m) * N1(pi*l/n, pi*m/n, k_e) + pi/n * N2(pi*l/n, pi*m/n, k_e))"),
        ("%i", "1.j"),
        ("J0_ir", "j0(gamma_ir * norm)"),
        ("J0_il", "j0(gamma_il * norm)"),
        ("H0_er", "hankel1(0, gamma_er * norm)"),
        ("H0_el", "hankel1(0, gamma_el * norm)"),
        ("J1_ir", "j1(gamma_ir * norm)"),
        ("J1_il", "j1(gamma_il * norm)"),
        ("H1_er", "hankel1(1, gamma_er * norm)"),
        ("H1_el", "hankel1(1, gamma_el * norm)"),
        ("H0_e", "hankel1(0, k_e * norm)"),
        ("H1_e", "hankel1(1, k_e * norm)"),
        ("J0_i", "j0(k_i * norm)"),
        ("J1_i", "j1(k_i * norm)"),
        ]
        s1 = s
        for r1, r2 in py_rules:
            s1 = s1.replace(r1, r2)
        return s1

    def make_parameters():
        if case == 'chiral_chiral':
            s = ur'''
c_il, c_ir, c_el, c_er = 1. + 1.j, 2.j, 1.-0.5j, 2.
omega = 5.
eps_i, mu_i, beta_i = 1.4, 1.2, 0.1
eps_e, mu_e, beta_e = 1.3, 1.25, 0.05'''

        elif case == 'chiral_achiral':
            s = ur'''
c_il, c_ir, c_el, c_er = 1. + 1.j, 3., 1., 2.
omega = 1.
eps_i, mu_i, beta_i = 1.4, 1.2, 0.
eps_e, mu_e, beta_e = 1.1, 1.15, 0.05'''

        elif case == 'achiral_chiral':
            s = ur'''
c_il, c_ir, c_el, c_er = 1. + 1.j, 3., 1., 2.
omega = 1.
eps_i, mu_i, beta_i = 1.4, 1.2, 0.1
eps_e, mu_e, beta_e = 1., 1., 0.'''

        elif case == 'chiral_conductor':
            s = ur'''
c_il, c_ir, c_el, c_er = 1. + 1.j, 3., 1., 2.
omega = 1.
eps_i, mu_i, beta_i = 1., 1., 0.
eps_e, mu_e, beta_e = 1.4, 1.2, 0.1'''

        elif case == 'achiral_chiral_gerlach':
            s = ur'''
c_il, c_ir, c_el, c_er = 1. + 1.j, 3., 1., 2.
omega = 1.
eps_i, mu_i, beta_i = 1.4, 1.2, 0.1
eps_e, mu_e, beta_e = 1., 1., 0.
c1, m1, c2, m2 = 1., 1., 2., 2.
xi = sqrt(eps_i*mu_e/(eps_e*mu_i))
xi_p = 1/2 * (xi + 1/xi)
xi_m = 1/2 * (xi - 1/xi)'''

        return s

    def make_u():
        s = ur'''%s
for l in arange(2*n):
    norm = x(l*pi/n)
    d_nu = (x2p(l*pi/n) * x1(l*pi/n) - x1p(l*pi/n) * x2(l*pi/n)) / (xp(l*pi/n) * norm)
%s'''
        sl = []
        indent = ' ' * 4
        if n == 2:
            declare = 'u = zeros((4*n,), dtype=complex)'
            for ii, i in enumerate(all_u):
                key = 'u[2*l + %s] = ' % ii
                sl.append(indent + key + py(i))

        elif n == 4:
            declare = 'u = zeros((8*n,), dtype=complex)'
            for ii, i in enumerate(all_u):
                key = 'u[4*l + %s] = ' % ii
                sl.append(indent + key + py(i))
              
        return s % (declare, '\n'.join(sl))

    def make_k():
        s = ur'''%s
for l in arange(2*n):
    for m in arange(2*n):
%s'''
        sl = []
        indent = ' ' * 8  
        if n == 2:
            declare = 'A = zeros((4*n, 4*n), dtype=complex)'
            for ii, i in enumerate(all_a):
                key = 'A[2*l + %s, 2*m + %s] = ' % (ii / n, ii % n)
                sl.append(indent + key + py(i)) 

        elif n == 4:
            declare = 'A = zeros((8*n, 8*n), dtype=complex)'
            for ii, i in enumerate(all_a):
                key = 'A[4*l + %s, 4*m + %s] = ' % (ii / n, ii % n)
                sl.append(indent + key + py(i)) 
            
        return s % (declare, '\n'.join(sl))

    def make_e():
        s = ur'''%s
for l in arange(2*n):
%s'''
        sl = []
        indent = ' ' * 4  
        if n == 2:
            declare = 'E = zeros((4*n, 4*n), dtype=complex)'
            for ii, i in enumerate(all_e):
                key = 'E[2*l + %s, 2*l + %s] = ' % (ii / n, ii % n)
                sl.append(indent + key + py(i)) 

        elif n == 4:
            declare = 'E = zeros((8*n, 8*n), dtype=complex)'
            for ii, i in enumerate(all_e):
                key = 'E[4*l + %s, 4*l + %s] = ' % (ii / n, ii % n)
                sl.append(indent + key + py(i)) 
            
        return s % (declare, '\n'.join(sl))

    def make_q():
        q_rules = [
        ("+", r" + "),
        ("-", r" - "),
        ("*", r" * "),
        ("/", r" / "),
        ("^", r" ** "),
        ("S_e_e", "(1.j * xp(l*pi/n))"),
        ("K_e_e", "(k_e * (d[0] * x2p(l*pi/n) - d[1] * x1p(l*pi/n)))"),
        ("S_g_el_e", "(1.j * xp(l*pi/n))"),
        ("S_g_er_e", "(1.j * xp(l*pi/n))"),
        ("K_g_el_e", "(gamma_el * (d[0] * x2p(l*pi/n) - d[1] * x1p(l*pi/n)))"),
        ("K_g_er_e", "(gamma_er * (d[0] * x2p(l*pi/n) - d[1] * x1p(l*pi/n)))"),
        ]

        sl = []
        if case == 'achiral_chiral_gerlach':
            q_rules.extend([('phi1', 'z[4*l]'), ('phi2', 'z[4*l+1]'), ('psi1', 'z[4*l+2]'), ('psi2', 'z[4*l+3]')])
        
        else:
            if n == 2:
                q_rules.extend([('psi1', 'z[2*l]'), ('psi2', 'z[2*l+1]')])

            elif n == 4:
                q_rules.extend([('psi1', 'z[4*l]'), ('psi2', 'z[4*l+1]'), ('psi3', 'z[4*l+2]'), ('psi4', 'z[4*l+3]')])
            
        def qq(s):
            s1 = s
            for r1, r2 in q_rules:
                s1 = s1.replace(r1, r2)
            return s1

        indent = ' ' * 4
        sl.append(indent + 'Q_er_inf += (%s) * exp(-1.j * gamma_er * (d[0] * x1(l*pi/n) + d[1] * x2(l*pi/n)))' % qq(all_q[0]))
        sl.append(indent + 'Q_el_inf += (%s) * exp(-1.j * gamma_el * (d[0] * x1(l*pi/n) + d[1] * x2(l*pi/n)))' % qq(all_q[1]))

        return '''
for l in arange(2*n):
%s
Q_er_inf = exp(-1j*pi/4) / sqrt(8*pi*gamma_er) * pi/n * Q_er_inf
Q_el_inf = exp(-1j*pi/4) / sqrt(8*pi*gamma_el) * pi/n * Q_el_inf''' % ('\n'.join(sl))
    
    if case.find('_3d') == -1 :
        open('em_%s_test.py' % case, 'w').write(code % (now, make_parameters(), make_indent(make_u()), make_indent(make_e()), make_indent(make_k()), make_indent(make_q()), case))

    open(os.path.join('data', 'em_%s.tex' % case), 'w').write(make_tex())
