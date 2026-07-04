% order5_0009  eq1=17366 eq2=35665  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(Y,Y),f(Y,f(X,f(X,Z)))) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(f(f(Y,f(X,Y)),f(Z,W)),W) )).
