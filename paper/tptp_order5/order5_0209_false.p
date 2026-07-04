% order5_0209  eq1=59341 eq2=14553  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( f(f(X,Y),X) = f(Y,f(f(Z,W),X)) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(Y,f(f(f(X,X),f(X,Z)),Z)) )).
