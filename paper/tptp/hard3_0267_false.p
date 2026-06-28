% hard3_0267  eq1=2525 eq2=2659  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(Y,f(f(X,Z),W)),X) )).
fof(neg, negated_conjecture, ? [X,Y] : ( X != f(f(f(X,Y),f(X,X)),X) )).
