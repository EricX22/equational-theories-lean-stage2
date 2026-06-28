% hard3_0099  eq1=761 eq2=2862  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(Y,f(Z,f(f(Y,Y),X))) )).
fof(neg, negated_conjecture, ? [X,Y] : ( X != f(f(f(X,f(Y,X)),X),X) )).
