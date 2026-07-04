% order5_0026  eq1=46488 eq2=16234  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( f(X,Y) = f(f(Z,X),f(W,f(W,W))) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(X,f(f(f(f(Y,Z),X),W),X)) )).
