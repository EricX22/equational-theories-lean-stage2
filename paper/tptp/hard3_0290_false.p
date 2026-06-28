% hard3_0290  eq1=2696 eq2=203  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y] : ( X = f(f(f(Y,X),f(X,X)),X) )).
fof(neg, negated_conjecture, ? [X] : ( X != f(f(X,f(X,X)),X) )).
