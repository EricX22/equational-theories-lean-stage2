% order5_0136  eq1=57265 eq2=47163  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( f(X,f(Y,Z)) = f(f(W,f(W,Z)),W) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,Y) != f(f(Y,X),f(f(Y,Z),Z)) )).
