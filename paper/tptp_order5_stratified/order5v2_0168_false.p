% order5v2_0168  eq1=24744 eq2=37857  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,W,X,Y,Z] : ( X = f(f(f(Y,Z),W),f(f(X,W),U)) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(f(f(Y,f(Z,f(Z,W))),X),W) )).
