function [Ex,Ey,Ez]=near_field_dipole_matrix_1(P0,M0,x0,y0,z0,x,y,z,thetaP,phiP,thetaM,phiM,etta0,c0,f)
% dipoles are in the same plane
m = length(y0);
n = length(z0);
Ex = 0;
Ey = 0;
Ez = 0;
for i = 1:m
    for j = 1:n
        [eex,eey,eez] = near_field_dipole_1(P0,M0,x0,y0(i),z0(j),x,y,z,thetaP,phiP,thetaM,phiM,etta0,c0,f);
        Ex = Ex+eex;
        Ey = Ey+eey;
        Ez = Ez+eez;
    end
end
end