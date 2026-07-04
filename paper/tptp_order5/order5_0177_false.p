% order5_0177  eq1=333 eq2=19853  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y] : ( f(X,Y) = f(Y,f(X,Y)) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(f(Y,X),f(f(Y,f(X,Z)),W)) )).
