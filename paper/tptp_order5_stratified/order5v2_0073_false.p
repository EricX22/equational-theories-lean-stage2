% order5v2_0073  eq1=35060 eq2=59999  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(f(Y,Z),f(f(X,Z),Z)),X) )).
fof(neg, negated_conjecture, ? [X,Y] : ( f(f(X,X),Y) != f(f(X,X),f(X,Y)) )).
