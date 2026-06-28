% hard3_0090  eq1=660 eq2=1848  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(X,f(Y,f(f(Z,Z),W))) )).
fof(neg, negated_conjecture, ? [X,Y] : ( X != f(f(X,f(Y,X)),f(X,Y)) )).
