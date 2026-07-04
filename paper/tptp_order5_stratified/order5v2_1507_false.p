% order5v2_1507  eq1=6586 eq2=3529  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(X,f(Y,f(f(Z,X),f(Z,W)))) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,Y) != f(X,f(f(Z,X),Y)) )).
