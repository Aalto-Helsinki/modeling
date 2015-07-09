
function [val] = crt_ycia(substrate,Kcat,Km)

val = Kcat.*substrate./(Km+substrate);

end