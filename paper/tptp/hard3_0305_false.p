% hard3_0305  eq1=2864 eq2=624  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(f(X,f(Y,X)),X),Z) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(X,f(X,f(f(Y,Y),Z))) )).
