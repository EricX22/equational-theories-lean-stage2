% hard3_0249  eq1=2262 eq2=1851  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(X,f(Y,f(X,Z))),W) )).
fof(neg, negated_conjecture, ? [X,Y] : ( X != f(f(X,f(Y,X)),f(Y,Y)) )).
