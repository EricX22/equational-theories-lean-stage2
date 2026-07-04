% order5_0102  eq1=3580 eq2=18898  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( f(X,Y) = f(Y,f(f(Z,W),W)) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(f(X,Y),f(f(Z,Z),f(Z,W))) )).
