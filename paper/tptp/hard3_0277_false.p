% hard3_0277  eq1=2660 eq2=3259  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y] : ( X = f(f(f(X,Y),f(X,X)),Y) )).
fof(neg, negated_conjecture, ? [X,Y] : ( f(X,X) != f(X,f(Y,f(X,Y))) )).
