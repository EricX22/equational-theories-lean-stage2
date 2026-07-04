% order5_0223  eq1=20836 eq2=57061  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y] : ( X = f(f(Y,Y),f(f(f(X,X),X),Y)) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(X,f(Y,Z)) != f(f(Y,f(Z,Y)),W) )).
