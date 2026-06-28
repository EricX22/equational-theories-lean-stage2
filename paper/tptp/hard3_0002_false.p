% hard3_0002  eq1=9 eq2=2441  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y] : ( X = f(X,f(X,Y)) )).
fof(neg, negated_conjecture, ? [X] : ( X != f(f(X,f(f(X,X),X)),X) )).
