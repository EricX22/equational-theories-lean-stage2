% order5v2_0020  eq1=36225 eq2=21794  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,W,X,Y,Z] : ( X = f(f(f(Y,f(Z,W)),f(W,U)),Y) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(Y,f(Y,Z)),f(X,f(Z,X))) )).
