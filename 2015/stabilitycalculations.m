% Simple stability analysis by analyzing eigenvalues of matrix A. Here we
% think the differential equations as x'(t) = A* x(t) +b(t), where x',x and
% b are vectors. This system is linear, so the method can be used.

% !! With long parameter vectors the calculations will get slow fast!

% Parameters we are interested in.
% I have no idea what these should be...... :D
nadphvec = [0.001,0.002,0.003,0.004,0.005,0.006,0.007,0.008,0.009,0.01];
nadhvec = [0.001,0.002,0.003,0.004,0.005,0.006,0.007,0.008,0.009,0.01];
h2ovec = [0.001,0.002,0.003,0.004,0.005,0.006,0.007,0.008,0.009,0.01];
atpvec = [0.001,0.002,0.003,0.004,0.005,0.006,0.007,0.008,0.009,0.01];
hvec = [0.001,0.002,0.003,0.004,0.005,0.006,0.007,0.008,0.009,0.01];
o2vec = [0.001,0.002,0.003,0.004,0.005,0.006,0.007,0.008,0.009,0.01];

% it is easy to make these vectors too and loop over them too to have more
% parameters to consider
k1 = 1;
k2 = 1;
k3 = 1;
k4 = 1;
k5 = 1;
k6 = 1;
k7 = 1;

% here are saved the parameters that give stable critical point
paramvec = [];
count = 1;

% calculations. 
for a=1:length(nadphvec)
    nadph = nadphvec(a);
    for b=1:length(nadhvec)
        nadh = nadhvec(b);
        for c=1:length(h2ovec)
            h2o = h2ovec(c);
            for d=1:length(atpvec)
                atp=atpvec(d);
                for e = 1:length(hvec)
                    h = hvec(e);
                    for f = 1:length(o2vec)
                        o2 = o2vec(f);
                        
                        % creating the A matrix
                        A = zeros(7);
                        vec = -[k2*nadph k3 k4*nadh k5*h2o k6*atp*h2o*nadph k7*nadph^2*h^2*o2];
                        A = A+diag([vec,0]);
                        A = A+diag(-vec,-1);
                        
                        % eigenvalues
                        E = eig(A);
                        
                        % Finding the real parts of eigenvalues, and finding all
                        % zero or positive of them. If there are none, the
                        % parameters are saved as columns in matrix.
                        if isempty(find(real(E) >= 0 )) % or perhaps >= -0.0000000000001 ?
                            paramvec(:,count)=[nadph; nadh; h2o; atp; h; o2; ...
                                k1; k2; k3; k4; k5; k6; k7];
                            count = count+1;
                        end
                    end
                end
            end
        end
    end
end

% how many stable critical points were found
[~,numberOfStableCriticalPoints]=size(paramvec);
fprintf('%d  stable critical points were found.\n',numberOfStableCriticalPoints)

% Saving the parameter vector if there are stable critical points
if(numberOfStableCriticalPoints > 0)
    save stabilityparams paramvec
end
