% order5_0187  eq1=2830 eq2=59525  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,W,X,Y,Z] : ( X = f(f(f(Y,Z),f(W,Y)),U) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(f(X,Y),Y) != f(Z,f(f(Y,Z),W)) )).
