% order5_0103  eq1=27108 eq2=17544  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,W,X,Y,Z] : ( X = f(f(f(Y,Y),f(Z,W)),f(Y,U)) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(f(Y,Z),f(X,f(W,f(W,X)))) )).
