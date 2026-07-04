% order5v2_0347  eq1=7941 eq2=49312  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,W,X,Y,Z] : ( X = f(Y,f(Z,f(f(Y,f(Y,W)),U))) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(X,Y) != f(f(f(Z,W),Y),f(Y,X)) )).
