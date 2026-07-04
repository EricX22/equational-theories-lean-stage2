% order5_0220  eq1=27119 eq2=31320  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,W,X,Y,Z] : ( X = f(f(f(Y,Y),f(Z,W)),f(U,X)) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(Y,f(f(X,Z),f(Z,Y))),X) )).
