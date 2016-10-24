size(200);

pen[] p={blue,green,blue,magenta};
path g=(0,0){dir(45)}..(1,0)..(1,1)..(0,1)..cycle;
tensorshade(rotate(-90, (0.5, 0.5))*g, p);

draw((0,0.55)--(0.6,0.55), Arrow);
label("$E_i,H_i$", (0.35, 0.65));
draw((0,0.55)--(-0.45,0.55), Arrow);
label("$E_e,H_e$", (-0.2, 0.65));
draw((-0.45, 0.45)--(0.04, 0.45), Arrow);
label("$E_o,H_o$", (-0.2, 0.35));

label("$\Omega_i$", (0.25, 0));
label("$\Omega_e$", (-0.2, 0));
label("$\Gamma$", (1, 0));

draw((1, 1)--(1.3, 1.11), Arrow);
label("$\nu$", (1.26, 1.16));

label("$\mu_i, \varepsilon_i, \beta_i$", (0.3, 1.1));
label("$\mu_e, \varepsilon_e, \beta_e$", (-0.3, 1.1));
