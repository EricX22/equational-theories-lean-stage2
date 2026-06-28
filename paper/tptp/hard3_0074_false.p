% hard3_0074  eq1=545 eq2=1832  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(Y,f(Z,f(X,f(Z,X)))) )).
fof(neg, negated_conjecture, ? [X] : ( X != f(f(X,f(X,X)),f(X,X)) )).
