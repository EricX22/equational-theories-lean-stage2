% order5v2_0814  eq1=26116 eq2=23422  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(Y,f(f(Y,X),Y)),f(Z,W)) )).
fof(neg, negated_conjecture, ? [U,W,X,Y,Z] : ( X != f(f(f(Y,X),Z),f(Y,f(W,U))) )).
