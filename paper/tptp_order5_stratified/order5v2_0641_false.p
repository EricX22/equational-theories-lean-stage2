% order5v2_0641  eq1=13266 eq2=29395  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(Y,f(f(Z,f(Z,f(Y,X))),Z)) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(X,f(Y,f(Z,f(Y,X)))),Y) )).
