% order5v2_1461  eq1=6082 eq2=48450  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(Y,f(Z,f(X,f(f(X,Y),Y)))) )).
fof(neg, negated_conjecture, ? [U,W,X,Y,Z] : ( f(X,Y) != f(f(Z,f(W,Y)),f(U,X)) )).
