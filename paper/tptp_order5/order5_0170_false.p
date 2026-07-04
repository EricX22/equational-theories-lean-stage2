% order5_0170  eq1=50371 eq2=56031  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( f(X,X) = f(f(Y,f(f(X,Z),X)),X) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,f(Y,Y)) != f(f(Z,Z),f(Z,X)) )).
