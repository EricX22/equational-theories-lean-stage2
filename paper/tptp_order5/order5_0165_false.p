% order5_0165  eq1=5549 eq2=25426  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,W,X,Y,Z] : ( X = f(Y,f(Z,f(W,f(U,f(Z,Z))))) )).
fof(neg, negated_conjecture, ? [U,W,X,Y,Z] : ( X != f(f(Y,f(Z,f(X,W))),f(X,U)) )).
