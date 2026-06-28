% hard3_0076  eq1=549 eq2=1966  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(Y,f(Z,f(X,f(W,X)))) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(Y,f(Z,X)),f(Z,X)) )).
