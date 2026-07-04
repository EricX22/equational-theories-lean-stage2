% order5v2_0222  eq1=20167 eq2=48920  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(Y,Z),f(f(X,f(W,Y)),Z)) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,Y) != f(f(f(Y,X),Z),f(X,Y)) )).
