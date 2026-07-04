% order5_0171  eq1=51104 eq2=14185  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( f(X,Y) = f(f(Z,f(f(W,Z),W)),Z) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(Y,f(f(Z,f(f(Z,W),Z)),X)) )).
