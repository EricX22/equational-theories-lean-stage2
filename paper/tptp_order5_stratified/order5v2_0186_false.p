% order5v2_0186  eq1=16569 eq2=34485  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(Y,f(f(f(f(Y,Z),Z),Z),W)) )).
fof(neg, negated_conjecture, ? [U,W,X,Y,Z] : ( X != f(f(f(Y,Z),f(W,f(U,Y))),W) )).
