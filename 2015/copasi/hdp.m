function [val] = hdp(A,kcat,kma,kmb)
nadph = 0.00012;

val = kcat.*A.*nadph./(A.*nadph+kmb.*A+kma.*nadph+kma.*kmb);

end

