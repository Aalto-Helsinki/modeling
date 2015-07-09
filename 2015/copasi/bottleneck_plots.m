close all

% Comparison of Hdb (blue) and Car (red)
figure(1)
plot([0:0.00001:0.006],hdp([0:0.00001:0.006],336.408402,5e-05,7e-05),'b')%201.8450412
hold on
plot([0:0.00001:0.006],car([0:0.00001:0.006],150,1.3e-05,4.8e-05,0.000115,1.3e-05),'r')
legend('Hbd','Car')

% Comparison of Crt, Ter (blue) and YciA
figure(2)
plot([0:0.00001:0.006],ter([0:0.00001:0.006],1881.62,2.7e-06,5.2e-06,1.98e-07),'b')
hold on
% crt
plot([0:0.00001:0.006],crt_ycia([0:0.00001:0.006],1168.85,7.5e-05),'r')
% ycia
plot([0:0.00001:0.006],crt_ycia([0:0.00001:0.006],1320,3.5e-06),'g')
legend('Ter','Crt','YciA')