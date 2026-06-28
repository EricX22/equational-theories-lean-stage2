% hard3_0006  eq1=38 eq2=4271  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y] : ( f(X,X) = f(X,Y) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,f(X,X)) != f(X,f(Y,Z)) )).
