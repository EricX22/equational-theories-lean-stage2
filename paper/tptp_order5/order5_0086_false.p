% order5_0086  eq1=20755 eq2=27668  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(Y,X),f(f(f(Y,Z),W),Z)) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(f(f(X,f(Y,Z)),Z),f(Z,W)) )).
