function star_quad_near_field()
%% Free Space charachteristic
u0 = 4*pi*1e-7; % permeability. 
epsi = 8.85e-12; % permittivity.
c0 = 299792458; % speed of light in free space.
etta0 = sqrt(u0/epsi);

%% Star quad cable parameters
s = 2.5e-3;
h = 1e-2;
rw = 0.25e-3;
p = 5e-2;
Lz = 1;
alpha = ((s/2)^2+(p/(2*pi))^2)^(-1/2);
L = 2*pi*Lz/alpha/p;

%% Averaged_per_unit_length_parameters
Ls = u0/(2*pi)*(log(2*h/rw)-s^2/(16*h^2));
L12 = u0/(2*pi)*(log(2*h/(s*abs(sin(pi/4))))-s^2/(16*h^2)*cos(1*pi/2));
L13 = u0/(2*pi)*(log(2*h/(s*abs(sin(pi/2))))-s^2/(16*h^2)*cos(pi));
LM = [Ls,L12,L13,L12;...
     L12,Ls,L12,L13;...
     L13,L12,Ls,L12;...
     L12,L13,L12,Ls];
Zc = c0*LM;

%% impedance
Ra = 100;
Rb = 100;
Rc = 100;
v  = [Ra Rb Ra Rb]; 
Zl = Rc*ones(4)+diag(v);
Zs = Zl;
%% other
LLS = [9.733,9.190,8.822,9.189;...
       9.191,9.323,8.770,8.901;...
       8.822,8.770,8.897,8.769;...
       9.189,8.901,8.769,9.320]*1e-9;
LRS = LLS;
TV = [1/4,1/4,1/4,1/4;...
     1/2,-1/2,1/2,-1/2;...
     1,0,-1,0;...
     0,1,0,-1];
TI = [1,1,1,1;...
     1/2,-1/2,1/2,-1/2;...
     1/2,0,-1/2,0;...
     0,1/2,0,-1/2];

%% Import Data
%% I0_Feko = load('10s909000.dat');

%% dipole
x0 = h; 
y0 = 10*s; 
z0 = Lz/2;
P0 = 10;
M0 = 10;
thetaP = deg2rad(90);
phiP = deg2rad(90);
thetaM = deg2rad(0);
phiM = deg2rad(0);

%% Twisting geometrical parameters
acc = 1e-5;
l = 0:acc:L;
len = length(l);
for i = 1:4
    x  = h+cos(alpha*l+(i-1)*pi/2).*(s/2);    
    dx = -alpha*sin(alpha*l+(i-1)*pi/2).*(s/2);
    y  = sin(alpha*l+(i-1)*pi/2).*(s/2);  
    dy = alpha*cos(alpha*l+(i-1)*pi/2).*(s/2);
    z  = alpha*l.*p/(2*pi);                                             
    dz = alpha*p/(2*pi);
     %% Frequency loop 
     index = 0; 
     for f = linspace(1e6,10e9,500)
        index = index+1;
        k = 2*pi*f/c0;  % The wave number.
        xL = linspace(0,x(1),len);
        xR = linspace(0,x(len),len);

        %% near field
        [Ex,Ey,Ez] = near_field_dipole_matrix_1(P0,M0,x0,y0,z0,x,y,z,thetaP,phiP,thetaM,phiM,etta0,c0,f);
        [ExL,EyL,EzL] = near_field_dipole_matrix_1(P0,M0,x0,y0,z0,xL,y(1),z(1),thetaP,phiP,thetaM,phiM,etta0,c0,f);
        [ExR,EyR,EzR] = near_field_dipole_matrix_1(P0,M0,x0,y0,z0,xR,y(len),z(len),thetaP,phiP,thetaM,phiM,etta0,c0,f);
        EEx(:,index) = Ex;
        EEy(:,index) = Ey;
        EEz(:,index) = Ez;
        %% VSLl and VSRl
        VF = Ex.*dx+Ey.*dy+Ez.*dz;
        SNC1 = sin(k*(l-L))/sin(k*L);
        SNC2 = sin(k*l)/sin(k*L);
        vSLl = trapz(l,SNC1.*VF);   
        VSLl(index) = vSLl;
        vSRl = trapz(l,SNC2.*VF);   
        VSRl(index) = vSRl;
        
        %% VSLv and VSRv
        % vSLv = -trapz(x1,SNC3);
        % VSLv(index) = vSLv;
        vSLv = -trapz(xL,ExL);
        VSLv(index) = vSLv;   
        vSRv = -trapz(xR,ExR);
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
    w = 2*pi*f;
    Zs1 = Zs+1j*w*LLS;
    Zl1 = Zl+1j*w*LRS;
    % Frequqncy Dependent Matrices
    PHI11 = cos(k*L)*eye(4);  
    PHI12 = -1j*Zc*sin(k*L);
    PHI21 = -1j*(Zc^-1)*sin(k*L);   
    PHI22 = cos(k*L)*eye(4);
    D = PHI11*Zs+Zl*PHI22-Zl*PHI21*Zs-PHI12;
    I01(:,index) = (D^-1)*((Zs*PHI21-PHI11)*VSL(:,index)+VSR(:,index));
    D = PHI11*Zs1+Zl1*PHI22-Zl1*PHI21*Zs1-PHI12;
    I02(:,index) = (D^-1)*((Zs1*PHI21-PHI11)*VSL(:,index)+VSR(:,index));

end
R = TI*I02;
ICM = R(1,:);
R = TI*I02;
IDM2 = R(2,:);
%%
figure();
f = linspace(1e6,10e9,500);
semilogx(f,20*log10(abs(ICM)),f,20*log10(abs(IDM2)),'linewidth',2);
%%hold on
%%semilogx(f,I0_Feko(:,2),'--','linewidth',2);
%%hold on
%%semilogx(f,I0_Feko(:,3),'--','linewidth',2);
%%hold on
legend('CM,analytical','DM,analytical','CM,Feko(MoM)','DM,Feko(MoM)');
xlabel('frequency(Hz)');
ylabel('modal current(dBA)');
end