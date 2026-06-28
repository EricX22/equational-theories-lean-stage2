% hard3_0017  eq1=72 eq2=214  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y] : ( X = f(Y,f(Y,f(X,X))) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(X,f(Y,Z)),X) )).
