function [Ex,Ey,Ez]=near_field_electric_dipole_1(P0,x0,y0,z0,x,y,z,theta,phi,etta0,c0,f)
%% near field of a electric dipole above a ground plane
    %%
    Py=P0*sin(theta)*cos(phi);
    Pz=P0*sin(theta)*sin(phi);
    Px=P0*cos(theta);
    %%
    P_scalar_R1=(x-x0).*Px+(y-y0).*Py+(z-z0).*Pz; 
    P_scalar_R2=(x+x0).*Px-(y-y0).*Py-(z-z0).*Pz;
    %%
    R1=sqrt((x-x0).^2+(y-y0).^2+(z-z0).^2);
    R2=sqrt((x+x0).^2+(y-y0).^2+(z-z0).^2);
    %%
    k=2*pi*f/c0 ;  % The wave number.
    PSI1=exp(-1j*k.*R1)./R1;
    PSI2=exp(-1j*k.*R2)./R2;
    [F1,G1]=near_field_Efactors(R1,f,c0);
    [F2,G2]=near_field_Efactors(R2,f,c0);
    %%        
    Ex=-1j*etta0.*k/(4*pi).*(F1*Px-G1.*(x-x0).*P_scalar_R1./(R1.^2)).*PSI1-1j*etta0.*k./(4*pi).*(F2*Px-G2.*(x+x0).*P_scalar_R2./(R2.^2)).*PSI2;     
    Ey=-1j*etta0.*k/(4*pi).*(F1*Py-G1.*(y-y0).*P_scalar_R1./(R1.^2)).*PSI1-1j*etta0.*k./(4*pi).*(-F2*Py-G2.*(y-y0).*P_scalar_R2./(R2.^2)).*PSI2; 
    Ez=-1j*etta0.*k/(4*pi).*(F1*Pz-G1.*(z-z0).*P_scalar_R1./(R1.^2)).*PSI1-1j*etta0.*k./(4*pi).*(-F2*Pz-G2.*(z-z0).*P_scalar_R2./(R2.^2)).*PSI2;
end