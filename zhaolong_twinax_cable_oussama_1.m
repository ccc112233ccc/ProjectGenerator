function [s_params2,sscd21,sscd11,sscc21,sscc11,ssdd21,ssdd11,f]=zhaolong_twinax_cable_oussama_1(rw,rsh,epsir,TanLoss,tsh,Lz,segmaAL,segmaCu,xd1,xd2,slot_d,fmin,fmax,Np)
%%%% Free Space charachteristic%%%%
u0=4*pi*1e-7 ;   % permeability. 
epsi=8.85e-12;   % permittivity.
c0=299792458 ;   % speed of light in free space.

% Ensure all inputs are double precision
rw = double(rw);
rsh = double(rsh);
epsir = double(epsir);
TanLoss = double(TanLoss);
tsh = double(tsh);
Lz = double(Lz);
segmaAL = double(segmaAL);
segmaCu = double(segmaCu);
xd1 = double(xd1);
xd2 = double(xd2);
slot_d = double(slot_d);
fmin = double(fmin);
fmax = double(fmax);

%%%%%% the cable parameters %%%%%%  
%rw=0.415e-3/2 ; % (m) 0.535e-3/2   0.24e-3   0.2075e-3   %The radius of the inner wires.
%D=1.42e-3  ;  % (m)   1.56e-3  1.42e-3     the distance between the signal lines
%h0=D;  %sqrt((D/2+rw)^2-(D/2)^2)  ; % (m)         %The distance between the ground and the coaxial cable.
%rsh=h0 ;  % the radius of the shield.
%epsir=2 ; % dielectric coating 2, (1.6219, exact cable)
%TanLoss=5e-4 ; % dilectic coating 5e-4
%tsh=9e-6; % (m)    % the thickness of the shield.  
%Lz=0.2 ;   %  (m)    0.2     %The total length of the coaxial cable.
%segmaAL=38160000 ;    %(s/m) %  the conductivity of the shield.
%segmaCu=58130000 ;    % (s/m) %  the conductivity of the wires
%xd1=D/2+0.05*D/2 ;  %+0.05*D/2 shifting the inner conductor 1 from the main coaxial axis
%xd2=-D/2 ; % shifting the inner conductor 2 from the main coaxial axis
%slot_d= 0.07e-3  ; % slot size  0.05e-3
%%%%Averaged_per_unit_length_parameters_inner_system%%%%
Delta1=(rw^2-xd1^2-rsh^2)^2-4*(xd1*rsh)^2 ;
alpha1=(-(rw^2-xd1^2-rsh^2)-sqrt(Delta1))/(2*xd1*rsh) ; 
F1=1/(pi*log(alpha1*(alpha1*xd1-rsh)/(xd1-alpha1*rsh))) ;
Delta2=(rw^2-xd2^2-rsh^2)^2-4*(xd2*rsh)^2 ;
alpha2=(-(rw^2-xd2^2-rsh^2)-sqrt(Delta2))/(2*xd2*rsh) ; 
F2=1/(pi*log(alpha2*(alpha2*xd2-rsh)/(xd2-alpha2*rsh))) ;
% Lin11=u0/(4*pi^2*F1) ;
% Lin22=u0/(4*pi^2*F2) ;
Lin11=u0/(2*pi)*log((rsh^2-xd1^2)/(rsh*rw)) ;
Lin22=u0/(2*pi)*log((rsh^2-xd2^2)/(rsh*rw)) ;
Lin12=u0/(2*pi)*log((1/rsh)*sqrt(((xd1*xd2)^2+rsh^4+2*abs(xd1*xd2)*rsh^2)/((xd1)^2+xd2^2+2*abs(xd1*xd2)))) ;

%%
delta=(rw^2-xd1^2-rsh^2)^2-4*(xd1*rsh)^2 ;
phi_a=deg2rad(0) ;
if xd1==0
alpha11=xd1/rsh ;   
else
alpha11=(-(rw^2-xd1^2-rsh^2)-sqrt(delta))/(2*xd1*rsh) ;  
end
%alpha=z0/b ;  
N=log((rsh^2-xd1^2)/(rw*rsh))/(2*pi) ;
A1=(1-alpha11^2)./(1+alpha11^2-2*alpha11*cos(phi_a)) ;
La1=u0*1/pi*(slot_d/(4*rsh))^2*A1^2 ;
Ca1=epsi*epsir/pi*(slot_d/(4*rsh*N))^2*A1^2 ;
%%
delta=(rw^2-xd2^2-rsh^2)^2-4*(xd2*rsh)^2 ; 
phi_a=deg2rad(0) ;
if xd2==0
alpha22=xd2/rsh ;   
else
alpha22=(-(rw^2-xd2^2-rsh^2)-sqrt(delta))/(2*xd2*rsh) ;  
end

N=log((rsh^2-xd2^2)/(rw*rsh))/(2*pi) ;
A2=(1-alpha22^2)./(1+alpha22^2-2*alpha22*cos(phi_a)) ;
La2=u0*1/pi*(slot_d/(4*rsh))^2*A2^2 ;
Ca2=epsi*epsir/pi*(slot_d/(4*rsh*N))^2*A2^2 ;
%%
LT=[Lin11  Lin12  ;  Lin12   Lin22] +[La1, 0 ; 0 , La2] ;
CT=(c0^-2)*(LT^-1)*epsir*(1-1j*TanLoss)-[Ca1 , 0 ; 0 , Ca2] ;
%
%%
%% Frequency loop 
    index=0 ; 
    for f=linspace(fmin,fmax,Np) 
        index=index+1;
    
      
      
        delta=1./sqrt(pi*f*u0*segmaCu);
%Rdc=1/(segma*pi*rw^2) ;
%q=sqrt(2)*rw./delta;
%[ber, bei, berd, beid] = kelvinb(0, q);
%Rac=Rdc*(q/2).*((ber.*beid-bei.*berd)./(berd.^2+beid.^2))   ;
a=rw ;
b=rsh ;
beta=(1+1j)./delta ;
Zac=(beta./(2*pi*segmaCu*rw)).*besseli(0,beta*rw)./besseli(1,beta*rw);
Delta=(a^2-xd1^2-b^2)^2-4*(xd1*b)^2 ;
% delta2=(a^2-z02^2-b^2)^2-4*(z02*b)^2 ;
alpha=(-(a^2-xd1^2-b^2)-sqrt(Delta))/(2*xd1*b) ; 
if xd1==0
    factor1=1 ;
else
factor1=alpha*(b^2-a^2-xd1^2)/(b*xd1*(1-alpha^2)) ;
end
CT1=Zac*factor1 ;
        %%
     
        %%
                delta=1./sqrt(pi*f*u0*segmaCu);
%Rdc=1/(segma*pi*rw^2) ;
%q=sqrt(2)*rw./delta;
%[ber, bei, berd, beid] = kelvinb(0, q);
%Rac=Rdc*(q/2).*((ber.*beid-bei.*berd)./(berd.^2+beid.^2))   ;
a=rw ;
b=rsh ;
beta=(1+1j)./delta ;
Zac=(beta./(2*pi*segmaCu*rw)).*besseli(0,beta*rw)./besseli(1,beta*rw);
Delta=(a^2-xd2^2-b^2)^2-4*(xd2*b)^2 ;
% delta2=(a^2-z02^2-b^2)^2-4*(z02*b)^2 ;
alpha=(-(a^2-xd2^2-b^2)-sqrt(Delta))/(2*xd2*b) ; 
if xd1==0
    factor2=1 ;
else
factor2=alpha*(b^2-a^2-xd2^2)/(b*xd2*(1-alpha^2)) ;
end
CT2=Zac*factor2 ;
        
        %%
   
       %%
       rw1=rw ;
       rw2=rw; 
       rshin=rsh ;
       rshout=rsh+tsh;
       segma_sh=segmaAL ;
       d1=xd1 ;
       d2=xd2 ;
       delta=1./sqrt(pi*f*u0*segma_sh);
       a1=rw1 ;
       a2=rw2;
      b=rshin ;
      z01=d1 ;
       z02=d2;
       beta=(1+1j)./delta ;
DELTA1=(a1^2-z01^2-b^2)^2-4*(z01*b)^2 ;
DELTA2=(a2^2-z02^2-b^2)^2-4*(z02*b)^2 ;
if z01==0
    alpha1=0 ;
else
alpha1=(-(a1^2-z01^2-b^2)-sqrt(DELTA1))/(2*z01*b) ; 
end
if z02==0
    alpha2=0 ;
else
alpha2=(-(a2^2-z02^2-b^2)-sqrt(DELTA2))/(2*z02*b) ; 
end
factor2=-besseli(1,beta*rshin,1).*besselk(1,beta*rshout,1).*exp(abs(real(beta*rshin))-beta*rshout)+besseli(1,beta*rshout,1).*besselk(1,beta*rshin,1).*exp(abs(real(beta*rshout))-beta*rshin) ;
F1=besselk(1,beta*rshout,1).*besseli(0,beta*rshin,1).*exp(abs(real(beta*rshin))-beta*rshout)+besseli(1,beta*rshout,1).*besselk(0,beta*rshin,1).*exp(abs(real(beta*rshout))-beta*rshin) ;
Ainsh=beta.*F1./(2*pi*segma_sh*rshin.*factor2) ;
Ainsh11=Ainsh*(1+alpha1^2)/(1-alpha1^2) ;
Binsh22=Ainsh*(1+alpha2^2)/(1-alpha2^2) ;
Cinsh12=Ainsh*(alpha1*(1-alpha2^2)-alpha2*(1-alpha1^2))/(alpha1*(1+alpha2^2)-alpha2*(1+alpha2^1)) ;
       %%
        AA=[Ainsh11, Cinsh12 ; Cinsh12 , Binsh22]+[CT1 , 0 ; 0 , CT2] ;
     %   R=[ZT1+R0, R0 ; R0 , ZT2+R0] ;
     %    R=0 ;
        Z=AA+1j*2*pi*f*LT ;
        Y=1j*2*pi*f*CT ;
        A=-[zeros(2) , Z ; Y , zeros(2)];
        DD=[1 1 -1 -1 ; 
            1 1 -1 -1 ; 
            1 1 -1 -1 ; 
            1 1 -1 -1] ;
        chaina=expm(-A*Lz) ;  ChainA(:,:,index)=chaina ;
        
        
    end
    %% Model Results
    s_params2 = abcd2s(ChainA,50); 
    [SDD, SDC, SCD, SCC] =s2smm(s_params2,2) ;  
    ssdd11(1,:)=SDD(1,1,:) ; 
    ssdd21(1,:)=SDD(2,1,:) ;
    sscc11(1,:)=SCC(1,1,:) ;
    sscc21(1,:)=SCC(2,1,:) ;
    sscd11(1,:)=SCD(1,1,:) ;
    sscd21(1,:)=SCD(2,1,:) ;
    f=linspace(fmin,fmax,Np);    

end