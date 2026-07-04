% order5v2_0233  eq1=27148 eq2=29527  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(f(Y,Z),f(X,Y)),f(Y,Z)) )).
fof(neg, negated_conjecture, ? [U,W,X,Y,Z] : ( X != f(f(Y,f(X,f(Y,f(Z,W)))),U) )).
