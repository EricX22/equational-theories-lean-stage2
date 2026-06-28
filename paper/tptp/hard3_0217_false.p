% hard3_0217  eq1=2049 eq2=215  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(f(X,X),Y),f(Z,W)) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(X,f(Y,Z)),Y) )).
