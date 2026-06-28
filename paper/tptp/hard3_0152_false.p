% hard3_0152  eq1=1252 eq2=1020  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y] : ( X = f(X,f(f(f(Y,Y),Y),Y)) )).
fof(neg, negated_conjecture, ? [X] : ( X != f(X,f(f(X,f(X,X)),X)) )).
