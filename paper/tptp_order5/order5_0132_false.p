% order5_0132  eq1=41818 eq2=26790  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( f(X,Y) = f(X,f(Z,f(X,f(W,X)))) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(f(X,Y),f(Z,Z)),f(Z,Z)) )).
