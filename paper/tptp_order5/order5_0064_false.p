% order5_0064  eq1=30472 eq2=54070  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(Y,f(X,f(f(Z,W),W))),Y) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(X,f(Y,X)) != f(Y,f(Z,f(X,W))) )).
