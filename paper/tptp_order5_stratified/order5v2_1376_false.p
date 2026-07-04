% order5v2_1376  eq1=18704 eq2=43925  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,W,X,Y,Z] : ( X = f(f(Y,Z),f(W,f(f(U,Z),Z))) )).
fof(neg, negated_conjecture, ? [U,W,X,Y,Z] : ( f(X,Y) != f(Z,f(f(Y,W),f(Y,U))) )).
