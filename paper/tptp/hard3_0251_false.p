% hard3_0251  eq1=2268 eq2=1851  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(X,f(Y,f(Y,Y))),Z) )).
fof(neg, negated_conjecture, ? [X,Y] : ( X != f(f(X,f(Y,X)),f(Y,Y)) )).
