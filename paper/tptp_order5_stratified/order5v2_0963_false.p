% order5v2_0963  eq1=25211 eq2=33428  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(Y,f(X,f(Z,W))),f(W,Z)) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(Y,f(f(f(Z,Z),X),Z)),Z) )).
