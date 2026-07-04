% order5v2_1567  eq1=9430 eq2=19671  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,W,X,Y,Z] : ( X = f(Y,f(f(X,Z),f(W,f(U,Z)))) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(X,Y),f(f(X,f(Y,Y)),Z)) )).
