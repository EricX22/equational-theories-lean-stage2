% order5v2_0369  eq1=15128 eq2=46453  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,W,X,Y,Z] : ( X = f(Y,f(f(f(Z,W),f(Y,U)),U)) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,Y) != f(f(Z,X),f(Z,f(X,X))) )).
