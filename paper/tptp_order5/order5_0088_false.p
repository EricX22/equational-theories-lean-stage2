% order5_0088  eq1=36918 eq2=9885  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(f(f(Y,Z),Y),f(W,W)),W) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(Y,f(f(Z,W),f(Z,f(W,Z)))) )).
