% order5_0218  eq1=15983 eq2=22697  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(Y,f(f(f(Z,f(W,Y)),X),Z)) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(Y,f(Y,Z)),f(f(Z,X),X)) )).
