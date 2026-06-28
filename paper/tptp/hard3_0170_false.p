% hard3_0170  eq1=1510 eq2=1163  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(Y,X),f(Z,f(W,X))) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(Y,f(f(Z,f(Y,X)),X)) )).
