% hard3_0394  eq1=4527 eq2=3439  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( f(X,f(Y,Z)) = f(f(Y,Y),X) )).
fof(neg, negated_conjecture, ? [U,W,X,Y,Z] : ( f(X,Y) != f(Z,f(W,f(Y,U))) )).
