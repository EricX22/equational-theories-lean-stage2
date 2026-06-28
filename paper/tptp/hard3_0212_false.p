% hard3_0212  eq1=2004 eq2=104  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(Y,f(Z,Z)),f(W,X)) )).
fof(neg, negated_conjecture, ? [X,Y] : ( X != f(X,f(f(Y,X),X)) )).
