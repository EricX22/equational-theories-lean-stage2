% order5v2_1599  eq1=29476 eq2=48301  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(Y,f(X,f(X,f(Z,X)))),Z) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(X,Y) != f(f(Z,f(Y,W)),f(X,X)) )).
