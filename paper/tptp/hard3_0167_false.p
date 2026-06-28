% hard3_0167  eq1=1487 eq2=3389  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(Y,X),f(X,f(Z,W))) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,Y) != f(Z,f(X,f(Z,Z))) )).
