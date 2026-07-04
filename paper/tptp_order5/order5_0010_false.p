% order5_0010  eq1=15649 eq2=54813  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(Y,f(f(f(Y,f(Z,X)),X),Z)) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(X,f(X,Y)) != f(Z,f(f(X,X),W)) )).
