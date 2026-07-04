% order5v2_0661  eq1=9811 eq2=33855  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,W,X,Y,Z] : ( X = f(Y,f(f(Z,Z),f(W,f(U,Y)))) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(f(Y,X),f(X,f(Y,Z))),X) )).
