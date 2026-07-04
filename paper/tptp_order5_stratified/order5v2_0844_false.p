% order5v2_0844  eq1=25734 eq2=6063  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,W,X,Y,Z] : ( X = f(f(Y,f(Z,f(W,U))),f(U,U)) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(Y,f(Y,f(Z,f(f(W,Z),Z)))) )).
