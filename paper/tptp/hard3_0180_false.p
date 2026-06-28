% hard3_0180  eq1=1594 eq2=2644  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(Y,Z),f(Z,f(Z,X))) )).
fof(neg, negated_conjecture, ? [X] : ( X != f(f(f(X,X),f(X,X)),X) )).
