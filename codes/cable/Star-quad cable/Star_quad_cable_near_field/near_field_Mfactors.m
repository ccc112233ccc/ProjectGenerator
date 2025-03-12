function [P,H]=near_field_Mfactors(R,f,c0)
%% near field factor 1 
    k=2*pi/c0*f;
    P=exp(-1j*k.*R)./R;
    H=1./R+1j.*k;
end

