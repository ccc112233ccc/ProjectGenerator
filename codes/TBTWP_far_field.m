function [ICM1,IDM11,f]=TBTWP_far_field(Lz,acc,pb,p,s,sb,rw,h,fmin,fmax,Np)

%%%% TBTWP cable  %%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%% Free Space charachteristic%%%%
u0=4*pi*1e-7 ;   % permeability. 磁导率
epsi=8.85e-12;   % permittivity. 介电常数
c0=299792458 ;   % speed of light in free space.
etta0=sqrt(u0/epsi);
%%%%%%  cable parameters %%%%%% 
%Lz=1 ;   %  (m)              %  TBTWP长度
%acc=0.0001;

%pb=25e-3;
%p=5e-3;


% pb=150e-3;
% p= 25e-3;

% pb=1000;   %%Untwisted wires
% p= 1000;

%%
% pb=100000;  %%对比
% p = 5e-3;

% pb=25e-3;  
% p= 100000;
%%

%s= 0.7e-3 ;
%sb=1.5e-3;
%rw=0.15e-3; % (m)         %The radius of the  wires.
% rw=0.1e-3;
%h=5e-3;

alpha_b=1/sqrt((sb/2)^2+(pb/(2*pi))^2);
Lb = 2*pi*Lz/(alpha_b*pb);            %单根TWP长度


alpha = 1/sqrt((s/2)^2+(p/(2*pi))^2);
alpha0 = alpha_b*alpha*p/(2*pi);
% L=2*pi*Lz/(alpha*p);         %%Lz:缠绕之后总长   L:拉伸总长
L=(2*pi)^2*Lz/(alpha_b*pb*alpha*p);   %单根导线长度

l=0:acc:L  ; 


h11= h+sb/2+s/2 ; % (m)         %The distance between the ground and the  cable. 
h12= h+sb/2-s/2 ;
h21= h-sb/2+s/2 ;
h22= h-sb/2-s/2 ;


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%Averaged_per_unit_length_parameters%%%%
L_11   =  u0/(2*pi)*log((2*h/rw)-(s^2+sb^2)/16*h^2);
L_1112 =  u0/(2*pi)*log((2*h/s)+(s^2+sb^2)/16*h^2);
L_1121 =  u0/(4*pi)*log(1+4*h^2/sb^2);

L_   = L_11;
L_M  = L_1112;
L_12 = L_1121;

Lsh=[L_,   L_M,  L_12, L_12;
     L_M,  L_,   L_12, L_12;
     L_12, L_12, L_,   L_M;
     L_12, L_12, L_M,  L_];

Csh = c0^(-2).*Lsh^-1;
Zc=c0.* Lsh ;  %The characteristic impedance of the outer system.
%%% input and output terminals of the shield %%%
Ra=49;
Rb=51;
Rc=100;

Zsh_SL=[Ra+Rc, Rc, 0, 0;
        Rc, Rb+Rc, 0, 0; 
        0, 0, Ra+Rc, Rc;
        0, 0, Rc, Rb+Rc ] ;  % left side 

        Zsh_SR= Zsh_SL;  % right side


%%%%% Plane-wave Characterization %%%%%%  远场激励（平面波）
E0=1       ;           %The electric field intensity of the incident field (v/m)
thetaE=deg2rad(90)   ; %Plarization angel.
thetaP=deg2rad(0)  ;   phiP=deg2rad(0) ;   %Direction of incidence. 

ex=sin(thetaE)*sin(thetaP) ; 
ey=-sin(thetaE)*cos(thetaP)*cos(phiP)-cos(thetaE)*sin(phiP) ; 
ez=-sin(thetaE)*cos(thetaP)*sin(phiP)+cos(thetaE)*cos(phiP) ;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%  
                x11 = h+(sb/2)*cos(alpha0*l)+s*cos(alpha*l)/2;
                x12 = h+(sb/2)*cos(alpha0*l)-s*cos(alpha*l)/2;
                x21 = h-(sb/2)*cos(alpha0*l)+s*cos(alpha*l)/2;
                x22 = h-(sb/2)*cos(alpha0*l)-s*cos(alpha*l)/2;
                
                y11 = (sb/2)*sin(alpha0*l)+s*sin(alpha*l)/2;
                y12 = (sb/2)*sin(alpha0*l)-s*sin(alpha*l)/2;
                y21 = -1*(sb/2)*sin(alpha0*l)+s*sin(alpha*l)/2;
                y22 = -1*(sb/2)*sin(alpha0*l)-s*sin(alpha*l)/2;
                
                z11 = pb*alpha_b*alpha*p*l/(2*pi)^2;
                z12 = z11;
                z21 = z11;
                z22 = z11;
               %% the unit tangent vectors for each wire
                eta11=sqrt(1+s*sb*alpha*alpha0*cos(alpha0*l-alpha*l)/2);
                eta12=sqrt(1-s*sb*alpha*alpha0*cos(alpha0*l-alpha*l)/2);
                eta21=sqrt(1-s*sb*alpha*alpha0*cos(alpha0*l-alpha*l)/2);
                eta22=sqrt(1+s*sb*alpha*alpha0*cos(alpha0*l-alpha*l)/2);
                
                n11_Lx=-1./eta11.*(1/2*sb*alpha0*sin(alpha0*l)+1/2*s*alpha*sin(alpha*l));
                n11_Ly=1./eta11.*(1/2*sb*alpha0*cos(alpha0*l)+1/2*s*alpha*cos(alpha*l));
                n11_Lz=alpha0*pb./(2*pi*eta11);
                
                n12_Lx=-1./eta12.*(1/2*sb*alpha0*sin(alpha0*l)-1/2*s*alpha*sin(alpha*l));
                n12_Ly=1./eta12.*(1/2*sb*alpha0*cos(alpha0*l)-1/2*s*alpha*cos(alpha*l));
                n12_Lz=alpha0*pb./(2*pi*eta12);
            
                n21_Lx=-1./eta21.*(-1/2*sb*alpha0*sin(alpha0*l)+1/2*s*alpha*sin(alpha*l));
                n21_Ly=1./eta21.*(-1/2*sb*alpha0*cos(alpha0*l)+1/2*s*alpha*cos(alpha*l));
                n21_Lz=alpha0*pb./(2*pi*eta21);

                n22_Lx=-1./eta22.*(1/2*sb*alpha0*sin(alpha0*l)+1/2*s*alpha*sin(alpha*l));
                n22_Ly=1./eta22.*(1/2*sb*alpha0*cos(alpha0*l)+1/2*s*alpha*cos(alpha*l));
                n22_Lz=alpha0*pb./(2*pi*eta22);
                %%
              %% LN  每根线求导
%                 x11_L = -1*(sb/2)*alpha0*sin(alpha0*l)-(s/2)*alpha*sin(alpha*l);
%                 x12_L = -1*(sb/2)*alpha0*sin(alpha0*l)+(s/2)*alpha*sin(alpha*l);
%                 x21_L = (sb/2)*alpha0*sin(alpha0*l)-(s/2)*alpha*sin(alpha*l);
%                 x22_L = (sb/2)*alpha0*sin(alpha0*l)+(s/2)*alpha*sin(alpha*l);
%                 
%                 y11_L = (sb/2)*alpha0*cos(alpha0*l)+(s/2)*alpha*cos(alpha*l);
%                 y12_L = (sb/2)*alpha0*cos(alpha0*l)-(s/2)*alpha*cos(alpha*l);
%                 y21_L = -1*(sb/2)*alpha0*cos(alpha0*l)+(s/2)*alpha*cos(alpha*l);
%                 y22_L = -1*(sb/2)*alpha0*cos(alpha0*l)-(s/2)*alpha*cos(alpha*l);
%                 
%                 z11_L = pb*alpha_b*alpha*p/(2*pi)^2;
%                 z12_L = z11_L;
%                 z21_L = z11_L;
%                 z22_L = z11_L;
                %%
%x=0:acc:h;
% x1=h1;
% x2=h2;
% y=0;

% z=0:acc:L;
%N=length(z);
%% Frequency loop 平面波的各方向分量EX,EY,EZ
    index=0 ; 
    for f=linspace(fmin,fmax,Np)
        index=index+1 ;        
                                
                k=2*pi*f/c0 ;  % The wave number.
                kx=-k*cos(thetaP) ;
                ky=-k*sin(thetaP)*cos(phiP) ;
                kz=-k*sin(thetaP)*sin(phiP) ;
                
                Ex11=2*E0*ex*cos(kx*x11).*exp(-1j*(ky*y11+kz*z11)) ;     
                Ey11=-2j*E0*ey*sin(kx*x11).*exp(-1j*(ky*y11+kz*z11)) ; 
                Ez11=-2j*E0*ez*sin(kx*x11).*exp(-1j*(ky*y11+kz*z11)) ; 
                
                Ex12=2*E0*ex*cos(kx*x12).*exp(-1j*(ky*y12+kz*z12)) ;     
                Ey12=-2j*E0*ey*sin(kx*x12).*exp(-1j*(ky*y12+kz*z12)) ; 
                Ez12=-2j*E0*ez*sin(kx*x12).*exp(-1j*(ky*y12+kz*z12)) ; 
                
                Ex21=2*E0*ex*cos(kx*x21).*exp(-1j*(ky*y21+kz*z21)) ;     
                Ey21=-2j*E0*ey*sin(kx*x21).*exp(-1j*(ky*y21+kz*z21)) ; 
                Ez21=-2j*E0*ez*sin(kx*x21).*exp(-1j*(ky*y21+kz*z21)) ; 
                
                Ex22=2*E0*ex*cos(kx*x22).*exp(-1j*(ky*y22+kz*z22)) ;     
                Ey22=-2j*E0*ey*sin(kx*x22).*exp(-1j*(ky*y22+kz*z22)) ; 
                Ez22=-2j*E0*ez*sin(kx*x22).*exp(-1j*(ky*y22+kz*z22)) ; 
                
            %%
                %双绞线对  TBTWP
                E11=Ex11.*n11_Lx+Ey11.*n11_Ly+Ez11.*n11_Lz;
                E12=Ex12.*n12_Lx+Ey12.*n12_Ly+Ez12.*n12_Lz;
                E21=Ex21.*n21_Lx+Ey21.*n21_Ly+Ez21.*n21_Lz;
                E22=Ex22.*n22_Lx+Ey22.*n22_Ly+Ez22.*n22_Lz;
                
%                 E11=Ex11.*x11_L+Ey11.*y11_L+Ez11.*z11_L;
%                 E12=Ex12.*x12_L+Ey12.*y12_L+Ez12.*z12_L;
%                 E21=Ex21.*x21_L+Ey21.*y21_L+Ez21.*z21_L;
%                 E22=Ex22.*x22_L+Ey22.*y22_L+Ez22.*z22_L;
                
                
                E=[E11;E12;E21;E22];
                
                %% the total induced  sources  
                PHI11=cos(k*L)*eye(4);          PHI12=-1j*Zc*sin(k*L) ;
                PHI21=-1j*(Zc^-1)*sin(k*L) ;    PHI22=cos(k*L)*eye(4) ;     %phi矩阵,平行线为phi(L-Z),双绞线为phi(L-l)
                Zcinv=inv(Zc);                         %计算Zc矩阵的逆矩阵
                %%
                VAG(1,:)=trapz(l,cos(k*(L-l)).*E(1,:));
                VAG(2,:)=trapz(l,cos(k*(L-l)).*E(2,:));
                VAG(3,:)=trapz(l,cos(k*(L-l)).*E(3,:));
                VAG(4,:)=trapz(l,cos(k*(L-l)).*E(4,:));
                
                
                IAG(1,:)=trapz(l,(-1j*(Zcinv(1,1)).*sin(k.*(L-l))).*E(1,:))+trapz(l,(-1j*(Zcinv(1,2)).*sin(k.*(L-l))).*E(2,:))+trapz(l,(-1j*(Zcinv(1,3)).*sin(k.*(L-l))).*E(3,:))+trapz(l,(-1j*(Zcinv(1,4)).*sin(k.*(L-l))).*E(4,:));
                IAG(2,:)=trapz(l,(-1j*(Zcinv(2,1)).*sin(k.*(L-l))).*E(1,:))+trapz(l,(-1j*(Zcinv(2,2)).*sin(k.*(L-l))).*E(2,:))+trapz(l,(-1j*(Zcinv(2,3)).*sin(k.*(L-l))).*E(3,:))+trapz(l,(-1j*(Zcinv(2,4)).*sin(k.*(L-l))).*E(4,:));
                IAG(3,:)=trapz(l,(-1j*(Zcinv(3,1)).*sin(k.*(L-l))).*E(1,:))+trapz(l,(-1j*(Zcinv(3,2)).*sin(k.*(L-l))).*E(2,:))+trapz(l,(-1j*(Zcinv(3,3)).*sin(k.*(L-l))).*E(3,:))+trapz(l,(-1j*(Zcinv(3,4)).*sin(k.*(L-l))).*E(4,:));
                IAG(4,:)=trapz(l,(-1j*(Zcinv(4,1)).*sin(k.*(L-l))).*E(1,:))+trapz(l,(-1j*(Zcinv(4,2)).*sin(k.*(L-l))).*E(2,:))+trapz(l,(-1j*(Zcinv(4,3)).*sin(k.*(L-l))).*E(3,:))+trapz(l,(-1j*(Zcinv(4,4)).*sin(k.*(L-l))).*E(4,:));
               %  IAG(2,:)=trapz(l,(-1j*(Zcinv(2,1)).*sin(k.*(L-l))).*E(1,:))+trapz(l,(-1j*(Zcinv(2,2)).*sin(k.*(L-l))).*E(2,:));
                
                

%                 n1=x1;
%                 n2=x2;
                n11=0:acc:h11;
                n12=0:acc:h12;
                n21=0:acc:h21;
                n22=0:acc:h22;
                 
                Vinc01=-trapz(n11,2*E0*ex*cos(kx*n11).*exp(-1j*(ky*y11(1)+kz*0)));
                Vinc02=-trapz(n12,2*E0*ex*cos(kx*n12).*exp(-1j*(ky*y12(1)+kz*0)));
                Vinc03=-trapz(n21,2*E0*ex*cos(kx*n21).*exp(-1j*(ky*y21(1)+kz*0)));
                Vinc04=-trapz(n22,2*E0*ex*cos(kx*n22).*exp(-1j*(ky*y22(1)+kz*0)));
                 
                VincL1=-trapz(n11,2*E0*ex*cos(kx*n11).*exp(-1j*(ky*y11(length(y11))+kz*L)));
                VincL2=-trapz(n12,2*E0*ex*cos(kx*n12).*exp(-1j*(ky*y12(length(y12))+kz*L)));
                VincL3=-trapz(n21,2*E0*ex*cos(kx*n21).*exp(-1j*(ky*y21(length(y21))+kz*L)));
                VincL4=-trapz(n22,2*E0*ex*cos(kx*n22).*exp(-1j*(ky*y22(length(y22))+kz*L)));
                

                Vinc0=[Vinc01;Vinc02;Vinc03;Vinc04];
                VincL=[VincL1;VincL2;VincL3;VincL4];

                VST=VAG+VincL-PHI11*Vinc0;
                IST=IAG-PHI21*Vinc0;




                %% Frequqncy Dependent Matrices
        %         PHI11=cos(k*L);  PHI12=-1j*Zc*sin(k*L) ;
        %         PHI21=-1j*(Zc^-1)*sin(k*L) ;  PHI22=cos(k*L) ; 


                A=PHI11*Zsh_SL+Zsh_SR*PHI22-PHI12-Zsh_SR*PHI21*Zsh_SL ;


                Iout_0=A^-1*(VST-Zsh_SR*IST) ;   IIout_0(:,index)=Iout_0 ;
                Vout_0=-Zsh_SL*Iout_0 ;          VVout_0(:,index)=Vout_0 ;
        %         
        %         Vout_z=cos(k*z)*Vout_0+(-1j*Zc*sin(k*z))*Iout_0+VST ;           VVout_z(index,:)=Vout_z ;
        %         Iout_z=(-1j*(Zc^-1)*sin(k*z))*Vout_0+cos(k*z)*Iout_0+IST ;      IIout_z(index,:)=Iout_z ;
        %         
        


    end
    %% results 
    f=linspace(fmin,fmax,Np);
    ICM1=IIout_0(1,:)+IIout_0(2,:);
    IDM11=(IIout_0(1,:)-IIout_0(2,:))/2;
   
      ICM1_phase=angle(ICM1)*180/pi;            %CM电流的相位，单位为：°
      IDM11_phase=angle(IDM11)*180/pi;          %DM电流的相位，单位为：°
    
    gcm = 20*log10(abs(ICM1));   %CM电流的幅值，单位为：dBA
    hdm = 20*log10(abs(IDM11));  %DM电流的幅值，单位为：dBA
    
%     a=load('two_wires_new1.dat');                   
%     a=xlsread('sample1.3.xlsx');

      
 
%        figure;
%        hold on , plot(f,gcm,'--','linewidth',2)      %MATLAB解析结果共模曲线
%        hold on , plot(f,hdm,'linewidth',2)           %MATLAB解析结果差模曲线
        
%         hold on , plot(f,ICM1_phase,'--','linewidth',2)      %MATLAB解析结果共模曲线
%         hold on , plot(f,IDM11_phase,'linewidth',2)           %MATLAB解析结果差模曲线
        
%         hold on , plot(f,fcm,'--','linewidth',2)    %画出共模曲线（FEKO）
%         hold on , plot(f,fdm,'--','linewidth',2)    %画出差模曲线(FEKO)
%        hold on;
        

%      legend('CM,传输线模型','DM,传输线模型','CM,MoM (FEKO)','DM,MoM (FEKO)');

%      legend('CM,MoM (FEKO)','DM,MoM (FEKO)');
%      legend('CM,Proposed Model','DM,Proposed Model');
%      legend('p=1mm 共模电流','p=2mm 共模电流','p=5mm 共模电流','p=10mm 共模电流','p=20mm 共模电流','p=50mm 共模电流','p=1000mm 共模电流');
%      legend('p=1mm 差模电流','p=2mm 差模电流','p=5mm 差模电流','p=10mm 差模电流','p=20mm 差模电流','p=50mm 差模电流','p=1000mm 差模电流');
%      legend('pb=10mm 共模电流','pb=10mm 差模电流','pb=20mm 共模电流','pb=20mm 差模电流','pb=40mm 共模电流','pb=40mm 差模电流','pb=80mm 共模电流','pb=80mm 差模电流','pb=160mm 共模电流','pb=160mm 差模电流','pb=320mm 共模电流','pb=320mm 差模电流','pb=1000mm 共模电流','pb=1000mm 差模电流');
%      legend('p=5mm 共模电流','p=5mm 差模电流','p=10mm 共模电流','p=10mm 差模电流','p=15mm 共模电流','p=15mm 差模电流','p=30mm 共模电流','p=30mm 差模电流','p=60mm 共模电流','p=60mm 差模电流','p=120mm 共模电流','p=120mm 差模电流','p=1000mm 共模电流','p=1000mm 差模电流');
%     set(gca,'XScale','log');
%    set(gca,'FontSize',16);
%     xlabel('Frequency (Hz)');
%     ylabel('Modal Currents Phase (Degree)');
%      ylabel('模式电流幅值 (dBA)');
%     grid on;
%     box on;
    
     
%      hold on ,plot(FrequencyHz,CurrentMagnitudeTBTWP_far_field909090_p10000000_pb25dBA);
%      hold on ,plot(FrequencyHz,Math);

     