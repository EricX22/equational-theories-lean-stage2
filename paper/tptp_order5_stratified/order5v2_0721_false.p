% order5v2_0721  eq1=31926 eq2=1674  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(X,f(f(X,f(Y,Z)),Z)),Y) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(X,Y),f(f(Z,Z),Z)) )).
