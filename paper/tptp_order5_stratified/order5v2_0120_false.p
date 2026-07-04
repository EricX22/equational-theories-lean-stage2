% order5v2_0120  eq1=16597 eq2=49176  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,W,X,Y,Z] : ( X = f(Y,f(f(f(f(Y,Z),W),U),Z)) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(X,Y) != f(f(f(Z,Y),Z),f(W,W)) )).
