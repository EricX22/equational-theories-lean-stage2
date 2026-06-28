% hard3_0350  eq1=3291 eq2=4480  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( f(X,X) = f(Y,f(Z,f(X,W))) )).
fof(neg, negated_conjecture, ? [X,Y] : ( f(X,f(Y,Y)) != f(f(Y,X),Y) )).
