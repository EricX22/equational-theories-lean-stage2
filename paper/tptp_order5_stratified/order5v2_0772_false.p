% order5v2_0772  eq1=39723 eq2=50924  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(f(f(Y,Z),f(W,W)),Z),Y) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,Y) != f(f(Z,f(f(Y,Z),Z)),Y) )).
