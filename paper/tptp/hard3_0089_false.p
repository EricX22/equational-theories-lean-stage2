% hard3_0089  eq1=652 eq2=3266  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(X,f(Y,f(f(Z,X),W))) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,X) != f(X,f(Y,f(Z,Z))) )).
