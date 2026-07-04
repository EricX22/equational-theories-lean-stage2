% order5v2_1828  eq1=9421 eq2=19447  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(Y,f(f(X,Z),f(W,f(Z,W)))) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(f(Y,Z),f(f(Z,W),f(Z,X))) )).
