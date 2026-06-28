% hard3_0263  eq1=2493 eq2=3052  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y] : ( X = f(f(Y,f(f(X,X),X)),X) )).
fof(neg, negated_conjecture, ? [X,Y] : ( X != f(f(f(f(X,X),X),Y),X) )).
