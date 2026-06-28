% hard3_0266  eq1=2521 eq2=1879  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(Y,f(f(X,Z),Z)),X) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(f(X,f(Y,Z)),f(W,X)) )).
