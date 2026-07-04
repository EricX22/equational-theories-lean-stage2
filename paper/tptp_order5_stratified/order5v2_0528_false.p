% order5v2_0528  eq1=8107 eq2=6865  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,W,X,Y,Z] : ( X = f(Y,f(Z,f(f(W,f(Y,W)),U))) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(Y,f(Y,f(f(Y,Z),f(Y,Y)))) )).
