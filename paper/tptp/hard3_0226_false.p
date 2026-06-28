% hard3_0226  eq1=2084 eq2=1430  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(f(X,Y),Z),f(W,Z)) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(X,X),f(X,f(Y,Z))) )).
