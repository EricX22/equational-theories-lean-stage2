% order5_0051  eq1=48447 eq2=50771  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( f(X,Y) = f(f(Z,f(W,Y)),f(W,Z)) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,Y) != f(f(Y,f(f(Z,Z),Z)),Z) )).
