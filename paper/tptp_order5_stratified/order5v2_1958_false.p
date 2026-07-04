% order5v2_1958  eq1=7956 eq2=44389  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(Y,f(Z,f(f(Y,f(Z,W)),Z))) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,Y) != f(X,f(f(X,f(Z,Y)),Z)) )).
