% order5_0071  eq1=35134 eq2=54782  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(f(Y,Z),f(f(Y,Z),Y)),Y) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(X,f(X,Y)) != f(Y,f(f(X,Z),W)) )).
