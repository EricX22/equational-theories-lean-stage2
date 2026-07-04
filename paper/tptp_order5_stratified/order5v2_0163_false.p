% order5v2_0163  eq1=2297 eq2=20932  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(Y,f(X,f(X,Z))),Y) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(Y,Y),f(f(f(Z,Y),Y),Z)) )).
