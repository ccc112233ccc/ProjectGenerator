function [Ex,Ey,Ez]=near_field_magnetic_dipole_1(M0,x0,y0,z0,x,y,z,theta,phi,c0,f)
%% near field of a electric dipole above a ground plane
    %%
    Mx = M0*cos(theta);
    My = M0*sin(theta)*cos(phi);
    Mz = M0*sin(theta)*sin(phi);
    %%
    R1 = sqrt((x-x0).^2+(y-y0).^2+(z-z0).^2);
    R2 = sqrt((x+x0).^2+(y-y0).^2+(z-z0).^2);
    %%
    [P1,H1] = near_field_Mfactors(R1,f,c0);
    [P2,H2] = near_field_Mfactors(R2,f,c0);
    %%
    Ex = H1.*P1./(4*pi.*R1).*(Mz.*(y-y0)-My.*(z-z0)) + H2.*P2./(4*pi.*R2).*(Mz.*(y-y0)-My.*(z-z0));
    Ey = H1.*P1./(4*pi.*R1).*(Mx.*(z-z0)-Mz.*(x-x0)) + H2.*P2./(4*pi.*R2).*(-Mx.*(z-z0)-Mz.*(x+x0));
    Ez = H1.*P1./(4*pi.*R1).*(My.*(x-x0)-Mx.*(y-y0)) + H2.*P2./(4*pi.*R2).*(My.*(x+x0)+Mx.*(y-y0));
end   
