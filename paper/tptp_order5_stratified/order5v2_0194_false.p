% order5v2_0194  eq1=1683 eq2=12880  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(Y,X),f(f(X,X),Z)) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(Y,f(f(X,f(Z,f(X,W))),W)) )).
