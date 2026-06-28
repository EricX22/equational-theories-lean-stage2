% hard3_0256  eq1=2410 eq2=2456  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(Y,f(Z,f(Z,W))),X) )).
fof(neg, negated_conjecture, ? [X,Y] : ( X != f(f(X,f(f(Y,X),X)),X) )).
