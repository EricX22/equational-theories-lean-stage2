% order5v2_0214  eq1=699 eq2=33774  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(Y,f(X,f(f(Z,W),Y))) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(f(f(X,Y),f(Z,f(X,W))),X) )).
