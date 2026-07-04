% order5v2_1377  eq1=37517 eq2=36223  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(f(Y,f(Y,f(X,Y))),Z),W) )).
fof(neg, negated_conjecture, ? [U,W,X,Y,Z] : ( X != f(f(f(Y,f(Z,W)),f(W,W)),U) )).
