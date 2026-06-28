% hard3_0135  eq1=1057 eq2=1454  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(X,f(f(Y,f(Z,X)),Z)) )).
fof(neg, negated_conjecture, ? [X,Y] : ( X != f(f(X,Y),f(Y,f(Y,X))) )).
