% order5v2_1632  eq1=32102 eq2=6185  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(Y,f(f(X,f(X,Y)),Z)),Y) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(Y,f(Z,f(Y,f(f(Y,W),Z)))) )).
