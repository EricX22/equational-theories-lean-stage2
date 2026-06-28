% hard3_0142  eq1=1092 eq2=176  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(Y,f(f(X,f(Z,X)),X)) )).
fof(neg, negated_conjecture, ? [X,Y] : ( X != f(f(Y,Y),f(X,X)) )).
