

function bottleneck_plots()

concentrations = [0:0.000001:0.002];

% Comparison of enzymes
figure
% AtoB                        enzyme Kcat        K_M
atobvals = atob(concentrations,1e-6,10653.02494,0.00047);
semilogy(concentrations,atobvals,'Color',[0,212/255,170/225],'LineWidth',2)
hold on
% Ter                                        enzyme Kcat K_MA   K_MB   K_iA     NADH
tervals = randombibiInhibition(concentrations,1e-6,5460,7e-05,5.2e-06,1.98e-07,8.3e-05);
semilogy(concentrations,tervals,'Color',[65/255,65/255,63/255],'LineWidth',2)
% ycia                                  enzyme Kcat K_M
yciavals = michaelisMenten(concentrations,1e-6,1320,3.5e-06);
semilogy(concentrations,yciavals,'Color',[0,163/255,203/225],'LineWidth',2)
% crt                                  enzyme Kcat    K_M
crtvals = michaelisMenten(concentrations,1e-6,1279.8,3e-05);
semilogy(concentrations,crtvals,'Color',[212/255,0/255,85/225],'LineWidth',2)
% hdb                              enzyme Kcat      K_MA  K_MB  NADPH
hbdvals = randombibi(concentrations,1e-6,336.408402,5e-5,7e-05,0.00012); 
semilogy(concentrations,hbdvals,'Color',[163/255,55/255,171/225],'LineWidth',2)
% Car                                        enzyme Kcat K_MA   K_MB    K_MC     K_iA
carvals = biuniunibipingpongCar(concentrations,1e-6,150,1.3e-02,4.8e-05,0.000115,0.013);
semilogy(concentrations,carvals,'Color',[255/255,42/255,63/225],'LineWidth',2)
% ADO                                  enzyme Kcat K_M
adovals = michaelisMenten(concentrations,1e-6,0.03,0.0101);
semilogy(concentrations,adovals,'Color',[175/255,219/255,0/225],'LineWidth',2)
% fadb2 approximated as better than it really is with irreversibility
%                                             enzyme Kcat   K_MA K_MB  K_iA  NADPH
fadb2vals = randombibiInhibition(concentrations,1e-6,0.677,0.656,0.50,0.656,0.00012);
semilogy(concentrations,fadb2vals,'Color',[43/255,154/255,133/225],'LineWidth',2)


title('Michaelis-Menten plots of propane pathway')

xlabel('Concentration of substrates, [mol/l] ([mmol/ml])') % x-axis label
ylabel('Speed of the reaction, [mol/min] ') % y-axis label

legend('AtoB','Ter','YciA','Crt','Hbd','Car','Ado','FadB2')



% Comparison of enzymes with enzyme concentration rates, ADO constuct is
% estimated to be expressed 1.5 times more
figure
% AtoB                        enzyme   Kcat       K_M
atobvals = atob(concentrations,1.5e-6,10653.02494,0.00047);
semilogy(concentrations,atobvals,'Color',[0,212/255,170/225],'LineWidth',2)
hold on
% Ter                                        enzyme Kcat K_MA   K_MB   K_iA     NADH
tervals = randombibiInhibition(concentrations,1.5e-6,5460,7e-05,5.2e-06,1.98e-07,8.3e-05);
semilogy(concentrations,tervals,'Color',[65/255,65/255,63/255],'LineWidth',2)
% crt                                   enzyme  Kcat    K_M
crtvals = michaelisMenten(concentrations,1.5e-6,1279.8,3e-05);
semilogy(concentrations,crtvals,'Color',[212/255,0/255,85/225],'LineWidth',2)
% ycia                                   enzyme Kcat   K_M
yciavals = michaelisMenten(concentrations,1e-6,1320,3.5e-06);
semilogy(concentrations,yciavals,'Color',[0,163/255,203/225],'LineWidth',2)
% hdb                              enzyme  Kcat      K_MA  K_MB  NADPH
hbdvals = randombibi(concentrations,1.5e-6,336.408402,5e-5,7e-05,0.00012); 
semilogy(concentrations,hbdvals,'Color',[163/255,55/255,171/225],'LineWidth',2)
% Car                                        enzyme Kcat K_MA   K_MB    K_MC     K_iA
carvals = biuniunibipingpongCar(concentrations,1e-6,150,1.3e-02,4.8e-05,0.000115,0.013);
semilogy(concentrations,carvals,'Color',[255/255,42/255,63/225],'LineWidth',2)
% ADO                                   enzyme Kcat  K_M
adovals = michaelisMenten(concentrations,1.5e-6,0.03,0.0101);
semilogy(concentrations,adovals,'Color',[175/255,219/255,0/225],'LineWidth',2)
% fadb2 approximated as better than it really is with irreversibility
%                                             enzyme  Kcat   K_MA K_MB  K_iA  NADPH
fadb2vals = randombibiInhibition(concentrations,1.5e-6,0.677,0.656,0.50,0.656,0.00012);
semilogy(concentrations,fadb2vals,'Color',[43/255,154/255,133/225],'LineWidth',2)


title('Michaelis-Menten plots of propane pathway (varying enzyme concentrations)')

xlabel('Concentration of substrates, [mol/l] ([mmol/ml])') % x-axis label
ylabel('Speed of the reaction, [mol/min] ') % y-axis label

legend('AtoB','Ter','Crt','YciA','Hbd','Car','Ado','FadB2')


end

function [val] = atob(substratea,enzyme,Kcat,Kma) % ping pong bi bi for AtoB

val = Kcat.*enzyme.*(substratea.*substratea)./ ...
    (substratea.*substratea+Kma.*substratea+Kma.*substratea);
end

function [val] = randombibi(A,enzyme,kcat,kma,kmb,substrateb)

val = kcat.*enzyme.*A.*substrateb./(A.*substrateb+kmb.*A+kma.*substrateb+kma.*kmb);

end

function [val] = biuniunibipingpongCar(substratea,enzyme,Kcat,Kma,Kmb,Kmc,Kia)

% this function is specific for Car, so these are defined here.. I could
% have so for all the K values but, whatever.
substrateb = 0.00012;
substratec = 0.0096;

val = (Kcat.*enzyme.*substratea.*substrateb.*substratec)./ ... 
    (Kia.*Kmb.*substratec+Kmc.*substratea.*substrateb+Kmb.*substratea.*substratec+ ... 
    Kma.*substrateb.*substratec+substratea.*substrateb.*substratec);
end

function [val] = randombibiInhibition(substratea,enzyme,Kcat,Kma,Kmb,Kia,substrateb)

val = (Kcat.*enzyme.*substratea.*substrateb)./ ...
    (substratea.*substrateb+Kmb.*substratea+Kma.*substrateb+Kia.*Kmb);
end

% These both are basic Michaelis-Menten
function [val] = michaelisMenten(substrate,enzyme,Kcat,Km)

val = Kcat.*enzyme.*substrate./(Km+substrate);

end