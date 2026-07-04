% order5v2_1317  eq1=33033 eq2=15865  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(Y,f(f(f(X,Y),Z),W)),Z) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(Y,f(f(f(Z,f(Y,W)),Z),W)) )).
