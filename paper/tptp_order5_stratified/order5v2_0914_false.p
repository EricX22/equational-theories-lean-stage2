% order5v2_0914  eq1=18497 eq2=16353  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,W,X,Y,Z] : ( X = f(f(Y,Z),f(Y,f(f(W,Z),U))) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(Y,f(f(f(f(X,Y),Y),Z),Y)) )).
