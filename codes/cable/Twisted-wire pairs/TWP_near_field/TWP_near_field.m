clear;clc;
%% Free Space charachteristic
u0 = 4*pi*1e-7; % permeability. 
epsi = 8.85e-12; % permittivity.
c0 = 299792458; % speed of light in free space.
etta0=sqrt(u0/epsi);

%% Twisted bundel parameters
s = 0.25e-2;
h = 1e-2;
rw = 0.25e-3;
p = 5e-2;
Lz = 1;
alpha = ((s/2)^2+(p/(2*pi))^2)^(-1/2);
L = 2*pi*Lz/alpha/p;

%% Electric Dipole Parameters
x0 = h; 
y0 = 100*s; 
z0 = 0.5;
P0 = 10;% electric dipole (A.m)
theta = deg2rad(0);
phi = deg2rad(0);

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
I0_Feko = load('20230905.dat');

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
    for f = linspace(1e6,10e9,500)
        index = index+1;
        k = 2*pi*f/c0;  % The wave number
        
        %% near field due to the electric dipole
        [Ex,Ey,Ez]=near_field_electric_dipole_1(P0,x0,y0,z0,x,y,z,theta,phi,etta0,c0,f);
        [Ex0,Ey0,Ez0]=near_field_electric_dipole_1(P0,x0,y0,z0,x,s/2*sin(alpha*L),Lz,theta,phi,etta0,c0,f);
        [ExL,EyL,EzL]=near_field_electric_dipole_1(P0,x0,y0,z0,x,-s/2*sin(alpha*L),Lz,theta,phi,etta0,c0,f);

        %% VSLl and VSRl
        VF = Ex.*dx+Ey.*dy+Ez.*dz;
        SNC1 = sin(k*(l-L))/sin(k*L);
        SNC2 = sin(k*l)/sin(k*L);
        vSLl = trapz(l,SNC1.*VF);   
        VSLl(index) = vSLl;
        vSRl = trapz(l,SNC2.*VF);   
        VSRl(index) = vSRl;

        %% VSLv and VSRv
        len = length(Ex0);
        x1 = linspace(0,x(1),len);
        x2 = linspace(0,x(len),len);
        vSLv = -trapz(x1,Ex0);
        VSLv(index) = vSLv;
        vSRv = -trapz(x2,ExL);
        VSRv(index) = vSRv;

    end
    VVSL = VSLl+VSLv;    
    VVSR = VSRl+VSRv; 
    VSL(i,:) = VVSL;    
    VSR(i,:) = VVSR; 
end

index = 0;
for f = linspace(1e6,10e9,500)
    index = index+1; 
    k = 2*pi*f/c0;
    %% Frequqncy Dependent Matrices
    PHI11 = cos(k*L)*eye(2);    
    PHI12 = -1j*Zc*sin(k*L);
    PHI21 = -1j*(Zc^-1)*sin(k*L);   
    PHI22 = cos(k*L)*eye(2);
    D = PHI11*Zs+Zl*PHI22-Zl*PHI21*Zs-PHI12;
    I0(:,index) = (D^-1)*((Zs*PHI21-PHI11)*VSL(:,index)+VSR(:,index));
    % IL(:,index) = (PHI22-PHI21*ZsL)*I0(:,index)-PHI21*VSL(:,index);
end
% figure();
f = linspace(1e6,10e9,500);
semilogx(f,20*log10(abs(I0(1,:)+I0(2,:))),f,20*log10(abs((I0(1,:)-I0(2,:)))/2),'linewidth',2);
hold on
semilogx(I0_Feko(:,1),I0_Feko(:,2),'--','linewidth',2);
hold on
semilogx(I0_Feko(:,1),I0_Feko(:,3),'--','linewidth',2);
legend('CM,analytical','DM,analytical','CM,Feko(MoM)','DM,Feko(MoM)');
xlabel('frequency(Hz)');
ylabel('modal current(dBA)');