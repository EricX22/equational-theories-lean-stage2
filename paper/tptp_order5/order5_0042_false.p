% order5_0042  eq1=55237 eq2=12114  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( f(X,f(Y,Z)) = f(X,f(f(Z,W),Z)) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(Y,f(f(f(Y,Y),Y),f(X,Z))) )).
