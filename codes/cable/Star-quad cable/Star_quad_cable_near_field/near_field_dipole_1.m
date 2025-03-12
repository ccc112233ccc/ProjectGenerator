function [Ex,Ey,Ez]=near_field_dipole_1(P0,M0,x0,y0,z0,x,y,z,thetaP,phiP,thetaM,phiM,etta0,c0,f)
    %% near field of a dipole matrix above a ground plane
    [ExP,EyP,EzP] = near_field_electric_dipole_1(P0,x0,y0,z0,x,y,z,thetaP,phiP,etta0,c0,f);
    [ExM,EyM,EzM] = near_field_magnetic_dipole_1(M0,x0,y0,z0,x,y,z,thetaM,phiM,c0,f);
    Ex = ExP+ExM;
    Ey = EyP+EyM;
    Ez = EzP+EzM;
end