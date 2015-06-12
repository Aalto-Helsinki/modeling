% Aalto-Helsinki 2015
% Riikka and Tuukka
% Sensitivity analysis by d[A]/d[B] where [] means concentration

function [] = sensitivityAnalysis(row)

if nargin <1
    row = 10000;
end

% Parameters, first concentrations what we assume constants
nadph = 1;
nadh = 1;
h2o = 1;
atp = 1;
h = 1;
o2 = 1;
a = 1;

% reaction rate constants
k1 = 0.47;
k2 = 0.05;
k3 = 0.03;
k4 = 0.0052;
k5 = 6.7;
k6 = 3.62;
k7 = 0.03;

% loading and selecting data
load concentrations.txt
first = concentrations(row,1:6);

% calculating the derivatives based on the data and constants (propane)
dB = dBdt(a,first(1,1),nadph,k1,k2);
dC = dCdt(first(1,1),first(1,2),nadph,k2,k3);
dD = dDdt(first(1,2),first(1,3),nadh,k3,k4);
dE = dEdt(first(1,3),first(1,4),h2o,nadh,k4,k5);
dF = dFdt(first(1,4),first(1,5),h2o,atp,nadph,k5,k6);
dG = dGdt(first(1,5),first(1,6),atp,h2o,nadph,h,o2,k6,k7);
dP = dPdt(first(1,6),nadph,h,o2,k7);

% data to vector format
vec1 = [dB,dC,dD, dE, dF, dG, dP];

% sensitivity matrix, containing d[I]/d[J] on row I and column J.
mat = dxdy(vec1)

% Bar plot
b = bar3(mat);
% cool colours
colormap('jet')
colorbar
for k = 1:length(b)
    zdata = b(k).ZData;
    b(k).CData = zdata;
    b(k).FaceColor = 'interp';
end
% naming the axis values for propane production
str = {'Acetoacetyl-CoA'; '3-hydr.-CoA'; 'Crotonyl-CoA'; 'Butyryl-Coa'; 'Butyric acid'; 'Butyraldehyde'; 'Propane'};
set(gca,'XTickLabel',str, 'XTick',1:numel(str));
set(gca,'YTickLabel',str, 'YTick',1:numel(str));

% Saving the matrix for future use
%save matrix mat
    
end


% Calculating the sensitivity matrix A, containing d[I]/d[J] on row I and 
% column J.
function [A] = dxdy(vec)
    n =length(vec);
    % combinations of vec
    mat = nchoosek(vec, 2);
    % calculating d[I]/d[J] (only half of them, lower trianglular half)
    divisions = mat(:, 1)./mat(:, 2);
    % putting d[I]/d[J] in matrix
    A = zeros(n);
    ind = 1;
    for ii=1:(n-1)
        A(1+ii:end, ii) = divisions(ind:ind+(n-ii)-1); 
        ind = ind + (n-ii);
    end
%     % calculating the upper triangular matrix for precision check
%     A2 = zeros(n);
%     divisions2 = mat(:,2)./mat(:,1);
%     ind2 = 1;
%     for jj = 1:(n-1)
%         A2(jj,(1+jj):end) = divisions2(ind2:ind2+(n-jj)-1);
%         ind2 = ind2+(n-jj);
%     end
    
    % Calculating upper triangular part of d[I]/d[J] matrix
    Aup = A.';
    Aup = triu(1./Aup,1);
    
%     A2
%     draft
%     max(max(abs(A2-draft)))
   
    % ready d[I]/d[J] matrix
    A = A + Aup + diag(ones(1,n));
end

% Reaction functions for propane production
function [dB] = dBdt(a,b,nadph,k1,k2)
    dB = k1*a^2-k2*b*nadph;
end

function [dC] = dCdt(b,c,nadph,k2,k3)
    dC = k2*b*nadph-k3*c;
end

function [dD] = dDdt(c,d,nadh,k3,k4)
    dD = k3*c-k4*d*nadh;
end

function [dE] = dEdt(d,e,h2o,nadh,k4,k5)
    dE = k4*d*nadh-k5*e*h2o;
end

function [dF] = dFdt(e,f,h2o,atp,nadph,k5,k6)
    dF = k5*e*h2o-k6*f*atp*h2o*nadph;
end

function [dG] = dGdt(f,g,atp,h2o,nadph,h,o2,k6,k7)
    dG = k6*f*atp*h2o*nadph-k7*g*nadph^2*h^2*o2;
end

function [dP] = dPdt(g,nadph,h,o2,k7)
    dP = k7*g*nadph^2*h^2*o2;
end