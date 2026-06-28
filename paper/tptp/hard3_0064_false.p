% hard3_0064  eq1=424 eq2=2466  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(X,f(X,f(Y,f(Z,Z)))) )).
fof(neg, negated_conjecture, ? [X,Y] : ( X != f(f(X,f(f(Y,Y),X)),X) )).
