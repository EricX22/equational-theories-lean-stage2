% hard3_0400  eq1=4579 eq2=4631  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,W,X,Y,Z] : ( f(X,f(Y,Z)) = f(f(W,U),Z) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(f(X,Y),X) != f(f(X,Z),X) )).
