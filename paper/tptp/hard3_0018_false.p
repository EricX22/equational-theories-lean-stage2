% hard3_0018  eq1=72 eq2=554  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y] : ( X = f(Y,f(Y,f(X,X))) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(Y,f(Z,f(Y,f(X,X)))) )).
