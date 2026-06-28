% hard3_0364  eq1=3514 eq2=4318  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( f(X,Y) = f(X,f(f(X,Z),X)) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,f(Y,X)) != f(X,f(Z,Z)) )).
