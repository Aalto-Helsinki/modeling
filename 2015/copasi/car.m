function [val] = car(substratea,Kcat,Kma,Kmb,Kmc,Kia)

substrateb = 0.00012;
substratec = 0.0096;

val = (Kcat.*substratea.*substrateb.*substratec)./ ... 
    (Kia.*Kmb.*substratec+Kmc.*substratea.*substrateb+Kmb.*substratea.*substratec+ ... 
    Kma.*substrateb.*substratec+substratea.*substrateb.*substratec);
end