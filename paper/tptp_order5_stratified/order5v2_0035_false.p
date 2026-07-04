% order5v2_0035  eq1=22655 eq2=58028  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(Y,f(Y,Y)),f(f(Z,Z),Y)) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(X,f(Y,Z)) != f(f(f(Z,W),X),W) )).
