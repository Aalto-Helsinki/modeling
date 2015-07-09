function [val] = ter(substratea,Kcat,Kma,Kmb,Kia)

substrateb = 8.3e-05;

val = (Kcat.*substratea.*substrateb)./ ...
    (substratea.*substrateb+Kmb.*substratea+Kma.*substrateb+Kia.*Kmb);
end