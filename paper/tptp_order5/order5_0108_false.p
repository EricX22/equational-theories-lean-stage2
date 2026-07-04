% order5_0108  eq1=39279 eq2=44508  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(f(f(Y,Y),f(X,Z)),Y),W) )).
fof(neg, negated_conjecture, ? [U,W,X,Y,Z] : ( f(X,Y) != f(X,f(f(Z,f(W,U)),X)) )).
