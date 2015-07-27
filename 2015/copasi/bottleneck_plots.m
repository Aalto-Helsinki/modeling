

function bottleneck_plots()

concentrations = [0:0.000001:0.002];

% Comparison of enzymes
figure
% hdb
hdbvals = hdp(concentrations,10e-6,336.408402,5e-5,7e-05); %336.408402, 5e-5
semilogy(concentrations,hdbvals,'b')%201.8450412
hold on
% fadb2
fadb2vals = fadb2(concentrations,10e-6,0.677,0.723,65.6,50,43.5,29.5); 
semilogy(concentrations,fadb2vals,'c')
hold on
% Car
carvals = car(concentrations,1e-6,150,1.3e-02,4.8e-05,0.000115,0.013);
semilogy(concentrations,carvals,'r')
% Ter
tervals = ter(concentrations,10e-6,1881.62,2.7e-06,5.2e-06,1.98e-07);
semilogy(concentrations,tervals,'m')
hold on
% crt
crtvals = crt_ycia(concentrations,10e-6,1310.812568,3e-05);
semilogy(concentrations,crtvals,'y')
% ycia
yciavals = crt_ycia(concentrations,1e-6,1320,3.5e-06);
semilogy(concentrations,yciavals,'g')
% AtoB
atobvals = atob(concentrations,10e-6,10653.02494,0.00047);
semilogy(concentrations,atobvals,'k')
% ADO
adovals = crt_ycia(concentrations,10e-6,0.215,0.0101);
semilogy(concentrations,adovals,'Color',[30/255,137/255,37/225])

title('Michaelis-Menten plots of propane pathway')

xlabel('Concentration of substrates, [mol/l] ([mmol/ml])') % x-axis label
ylabel('Speed of the reaction, [mol/min] ') % y-axis label

legend('Hbd','FadB2','CAR','Ter','Crt','YciA','AtoB','ADO')


save bottleneck concentrations hdbvals fadb2vals carvals tervals crtvals yciavals atobvals adovals

end

function [val] = fadb2(substratea,enzyme,Kcat1, Kcat2, Kma, Kmb, Kmpa, Kmpb)

substrateb = 0.00012;
producta = 2.35473e-16; % this value is taken from time 100 min in Copasi time series estimation
% unfortunately 3-hydroxybutyryl-CoA is not constant, but slightly
% increasing all the time so that might not be a good value for it.
% However, I didn't think of a better way to estimate this.
productb = 2.1e-06; % this also rises all the time in the Copasi model, 
% however since it it used also in other places in the cell the estimation
% of normal value in the cell is more justified.
Keq = 1;

val = (substratea.*substrateb-(producta.*productb)./Keq)./ ...
    ((Kma.*Kmb)./(Kcat1.*enzyme)+(Kmb.*substratea)./(Kcat1.*enzyme)+...
    (Kma.*substrateb)./(Kcat1.*enzyme)+(Kmpa.*productb)./(Keq.*Kcat2.*enzyme)+ ...
    (Kmpb.*producta)./(Keq.*Kcat2.*enzyme)+ ...
    (substratea.*substrateb)./(Kcat1.*enzyme)+ ...
    (productb.*producta)./(Keq.*Kcat2.*enzyme));

end

function [val] = atob(substratea,enzyme,Kcat,Kma)

val = Kcat.*enzyme.*(substratea.*substratea)./ ...
    (substratea.*substratea+Kma.*substratea+Kma.*substratea);
end

function [val] = hdp(A,enzyme,kcat,kma,kmb)
nadph = 0.00012;

val = kcat.*enzyme.*A.*nadph./(A.*nadph+kmb.*A+kma.*nadph+kma.*kmb);

end

function [val] = car(substratea,enzyme,Kcat,Kma,Kmb,Kmc,Kia)

substrateb = 0.00012;
substratec = 0.0096;

val = (Kcat.*enzyme.*substratea.*substrateb.*substratec)./ ... 
    (Kia.*Kmb.*substratec+Kmc.*substratea.*substrateb+Kmb.*substratea.*substratec+ ... 
    Kma.*substrateb.*substratec+substratea.*substrateb.*substratec);
end

function [val] = ter(substratea,enzyme,Kcat,Kma,Kmb,Kia)

substrateb = 8.3e-05;

val = (Kcat.*enzyme.*substratea.*substrateb)./ ...
    (substratea.*substrateb+Kmb.*substratea+Kma.*substrateb+Kia.*Kmb);
end

% These both are basic Michaelis-Menten
function [val] = crt_ycia(substrate,enzyme,Kcat,Km)

val = Kcat.*enzyme.*substrate./(Km+substrate);

end