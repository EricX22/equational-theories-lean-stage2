% order5v2_1781  eq1=26079 eq2=54694  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(Y,f(f(X,Z),W)),f(Y,W)) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,f(X,X)) != f(X,f(f(Y,Y),Z)) )).
