clear;clc;
%% Free Space charachteristic
u0 = 4*pi*1e-7; % permeability. 
epsi = 8.85e-12; % permittivity.
c0 = 299792458; % speed of light in free space.

%% Twisted bundel parameters
s = 0.25e-2;
h = 1e-2;
rw = 1.46e-9;
p = 5e-2;
Lz = 1;
alpha = ((s/2)^2+(p/(2*pi))^2)^(-1/2);
L = 2*pi*Lz/alpha/p;

%% Averaged_per_unit_length_parameters
Ra = 50; Rb = 50; Rc = 100;
l_avg  = u0/(2*pi)*log(2*h/rw);
lm_avg = u0/(2*pi)*(log(2*h/s)+s^2/(16*h^2));
L_avg  = [l_avg,lm_avg;lm_avg,l_avg];
C_avg  = (1/(c0^2))*L_avg;
Zc = c0*L_avg;

Zl = [Ra+Rc,Rc;Rc,Rb+Rc];
Zs = [Ra+Rc,Rc;Rc,Rb+Rc];

Zc_vr = c0*u0/(2*pi)*(log(2*h/rw)-1);  
L_vr = h*Zc_vr/c0;
Zc_dr = c0*u0/(2*pi)*log(s/rw);

%% Import Data
I0_Feko = load('endfire.dat');

%% Plane-wave Characterization
E0 = 1;
%Side-fire
% thetaE = deg2rad(0);
% thetaP = deg2rad(0);   
% phiP = deg2rad(0);
%End-Fire
thetaE = deg2rad(90);
thetaP = deg2rad(90);   
phiP = deg2rad(-90);
%Broad-Side
% thetaE = deg2rad(90);
% thetaP = deg2rad(90);   
% phiP = deg2rad(0);
ex = sin(thetaE)*sin(thetaP); 
ey = -sin(thetaE)*cos(thetaP)*cos(phiP)-cos(thetaE)*sin(phiP); 
ez = -sin(thetaE)*cos(thetaP)*sin(phiP)+cos(thetaE)*cos(phiP);

%% Twisting geometrical parameters
acc = 1e-5;
l = 0:acc:L;
for i = 1:2
    x  = h+(cos(alpha*l).*(s/2)*((-1)^(i-1)));    
    dx = -(alpha*sin(alpha*l).*(s/2)*((-1)^(i-1)));
    y  = sin(alpha*l).*(s/2)*((-1).^(i-1));      
    dy = alpha*cos(alpha*l).*(s/2)*(-1)^(i-1);
    z  = alpha*l.*p/(2*pi);                                             
    dz = alpha*p/(2*pi);

    %% Frequency loop 
    index = 0; 
    for f = linspace(1e6,1e9,1000)
        index = index+1;
        k = 2*pi*f/c0;  % The wave number.
        kx=-k*cos(thetaP);
        ky=-k*sin(thetaP)*cos(phiP);
        kz=-k*sin(thetaP)*sin(phiP);
        Ex=2*E0*ex*cos(kx*x).*exp(-1j*(ky*y+kz*z));     
        Ey=-2j*E0*ey*sin(kx*x).*exp(-1j*(ky*y+kz*z)); 
        Ez=-2j*E0*ez*sin(kx*x).*exp(-1j*(ky*y+kz*z)); 
        
        %% VSLl and VSRl
        VF = Ex.*dx+Ey.*dy+Ez.*dz;
        SNC1 = sin(k*(l-L))/sin(k*L);
        SNC2 = sin(k*l)/sin(k*L);
        vSLl = trapz(l,SNC1.*VF);   
        VSLl(index) = vSLl;
        vSRl = trapz(l,SNC2.*VF);   
        VSRl(index) = vSRl;
        
        %% VSLv and VSRv
        vSLv = -2*E0*ex*sin(kx*x(1))/kx;
        VSLv(index) = vSLv;
        vSRv = -2*E0*ex*sin(kx*x(length(x))).*exp(-1j*(ky*y(length(y))+kz*Lz))/kx;
        VSRv(index) = vSRv;

        %% Riser Current   
        VarName_L1 = 0; VarName_R1 = 0;
        Zrr = Zc_vr*(0+1j*Zc_vr*tan(k*h))/(Zc_vr+1j*0*tan(k*h))+Rc;
        Ivr0 = -1j*k*h^2*E0*ex*exp(-1j*kz*0)/Zc_vr-1j*k*s^2*(VarName_L1)/(8*Zc_dr);  
        IvrL = -1j*k*h^2*E0*ex*exp(-1j*kz*Lz)/Zc_vr-1j*k*s^2*(VarName_R1)/(8*Zc_dr); 
        Idr0 = -1j*k*(s/2)^2*E0*ex*exp(-1j*kz*0)/Zc_dr; 
        IdrL = -1j*k*(s/2)^2*E0*ex*exp(-1j*kz*Lz)/Zc_dr;
        vris0 = Zrr*Ivr0+(Ra*((-1)^(i+1)+1)/2-Rb*((-1)^(i)+1)/2)*Idr0;   
        Vris0(index) = vris0;  
        vrisL = Zrr*IvrL+(Ra*((-1)^(i+1)+1)/2-Rb*((-1)^(i)+1)/2)*IdrL;   
        VrisL(index) = vrisL; 
    end
    VVSL = VSLl+VSLv;    
    VVSR = VSRl+VSRv; 
    VSL(i,:) = VVSL;    
    VSR(i,:) = VVSR; 
end

index = 0;
for f = linspace(1e6,1e9,1000)
    index = index+1; 
    k = 2*pi*f/c0;
    %% Frequqncy Dependent Matrices
    PHI11 = cos(k*L)*eye(2);    
    PHI12 = -1j*Zc*sin(k*L);
    PHI21 = -1j*(Zc^-1)*sin(k*L);   
    PHI22 = cos(k*L)*eye(2);
    Zr = Zc_vr*(0+1j*Zc_vr*tan(k*h))/(Zc_vr+1j*0*tan(k*h));
    Zl1 = Zl+Zr*ones(2);
    Zs1 = Zl1;
    D = PHI11*Zs+Zl*PHI22-Zl*PHI21*Zs-PHI12;
    I0(:,index) = (D^-1)*((Zs*PHI21-PHI11)*VSL(:,index)+VSR(:,index));
end
figure();
f = linspace(1e6,1e9,1000);
semilogx(f,20*log10(abs(I0(1,:)+I0(2,:))),f,20*log10(abs((I0(1,:)-I0(2,:)))/2),'linewidth',2);
hold on
semilogx(I0_Feko(:,1),I0_Feko(:,2),'--','linewidth',2);
hold on
semilogx(I0_Feko(:,1),I0_Feko(:,3),'--','linewidth',2);
title('End-Fire');
legend('CM, analytical','DM, analytical','CM, Feko (MoM)','DM, Feko (MoM)');
xlabel('Frequency (Hz)');
ylabel('Modal Current (dBA)');