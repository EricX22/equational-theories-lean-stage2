% hard3_0009  eq1=48 eq2=2255  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y] : ( X = f(X,f(X,f(X,Y))) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(X,f(Y,f(X,X))),Z) )).
