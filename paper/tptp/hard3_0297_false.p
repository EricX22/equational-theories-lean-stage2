% hard3_0297  eq1=2831 eq2=2060  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(f(Y,Z),f(W,Z)),X) )).
fof(neg, negated_conjecture, ? [X,Y] : ( X != f(f(f(X,Y),Y),f(X,X)) )).
