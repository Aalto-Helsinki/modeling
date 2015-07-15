

function bottleneck_plots()

% Comparison of enzymes
figure
% hdb
plot([0:0.000001:0.002],hdp([0:0.000001:0.002],336.408402,5e-05,7e-05),'b')%201.8450412
hold on
% Car
plot([0:0.000001:0.002],car([0:0.000001:0.002],150,1.3e-05,4.8e-05,0.000115,1.3e-05),'r')
% Ter
plot([0:0.000001:0.002],ter([0:0.000001:0.002],1881.62,2.7e-06,5.2e-06,1.98e-07),'m')
hold on
% crt
plot([0:0.000001:0.002],crt_ycia([0:0.000001:0.002],1168.85,7.5e-05),'y')
% ycia
plot([0:0.000001:0.002],crt_ycia([0:0.000001:0.002],1320,3.5e-06),'g')
% AtoB
plot([0:0.000001:0.002],crt_ycia([0:0.000001:0.002],20418.3,0.00047),'k')
legend('Hbd','Car','Ter','Crt','YciA','AtoB')

end

function [val] = atob(substratea,Kcat,Kma)

val = Kcat.*(substratea.*substratea)./ ...
    (substratea.*substratea+Kma.*substratea+Kma.*substratea);
end

function [val] = hdp(A,kcat,kma,kmb)
nadph = 0.00012;

val = kcat.*A.*nadph./(A.*nadph+kmb.*A+kma.*nadph+kma.*kmb);

end

function [val] = car(substratea,Kcat,Kma,Kmb,Kmc,Kia)

substrateb = 0.00012;
substratec = 0.0096;

val = (Kcat.*substratea.*substrateb.*substratec)./ ... 
    (Kia.*Kmb.*substratec+Kmc.*substratea.*substrateb+Kmb.*substratea.*substratec+ ... 
    Kma.*substrateb.*substratec+substratea.*substrateb.*substratec);
end

function [val] = ter(substratea,Kcat,Kma,Kmb,Kia)

substrateb = 8.3e-05;

val = (Kcat.*substratea.*substrateb)./ ...
    (substratea.*substrateb+Kmb.*substratea+Kma.*substrateb+Kia.*Kmb);
end

% These both are basic Michaelis-Menten
function [val] = crt_ycia(substrate,Kcat,Km)

val = Kcat.*substrate./(Km+substrate);

end