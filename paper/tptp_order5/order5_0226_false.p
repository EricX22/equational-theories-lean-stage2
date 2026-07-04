% order5_0226  eq1=14942 eq2=19167  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(Y,f(f(f(Z,Y),f(Y,X)),Y)) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(f(Y,Y),f(f(Z,X),f(W,X))) )).
