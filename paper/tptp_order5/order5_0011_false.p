% order5_0011  eq1=10945 eq2=8630  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(X,f(f(Y,f(Y,Z)),f(X,Z))) )).
fof(neg, negated_conjecture, ? [U,W,X,Y,Z] : ( X != f(Y,f(Y,f(f(f(Y,Z),W),U))) )).
