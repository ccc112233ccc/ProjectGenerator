function [F,G]=near_field_factors(R,f,c0)
%% near field factor 1 
    k=2*pi*f/c0;
    F=1+1./(1j*k*R)-1./(k^2*R.^2);
    G=1+3./(1j*k*R)-3./(k^2*R.^2);
end