% hard3_0114  eq1=922 eq2=1444  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(Y,f(f(Y,Y),f(Z,X))) )).
fof(neg, negated_conjecture, ? [X,Y] : ( X != f(f(X,Y),f(X,f(Y,X))) )).
