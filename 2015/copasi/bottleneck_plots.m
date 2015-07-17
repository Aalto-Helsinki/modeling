

function bottleneck_plots()

concentrations = [0:0.000001:0.002];

% Comparison of enzymes
figure
% hdb
hdbvals = hdp(concentrations,0.677,0.0656,7e-05); %336.408402, 5e-5
semilogy(concentrations,hdbvals,'b')%201.8450412
hold on
% Car
carvals = car(concentrations,150,1.3e-02,4.8e-05,0.000115,1.3e-05);
semilogy(concentrations,carvals,'r')
% Ter
tervals = ter(concentrations,1881.62,2.7e-06,5.2e-06,1.98e-07);
semilogy(concentrations,tervals,'m')
hold on
% crt
crtvals = crt_ycia(concentrations,1168.85,7.5e-05);
semilogy(concentrations,crtvals,'y')
% ycia
yciavals = crt_ycia(concentrations,1320,3.5e-06);
semilogy(concentrations,yciavals,'g')
% AtoB
atobvals = atob(concentrations,20418.3,0.00047);
semilogy(concentrations,atobvals,'k')

title('Michaelis-Menten plots of propane pathway')

xlabel('Concentration of substrates, [mol/l] ([mmol/ml])') % x-axis label
ylabel('Speed of the reaction, [1/min] ') % y-axis label

legend('Hbd','Car','Ter','Crt','YciA','AtoB')


save bottleneck concentrations hdbvals carvals tervals crtvals yciavals atobvals

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