% order5_0167  eq1=16782 eq2=40530  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(Y,f(f(f(f(Z,Z),Y),Z),Z)) )).
fof(neg, negated_conjecture, ? [U,W,X,Y,Z] : ( X != f(f(f(f(Y,f(Z,W)),X),W),U) )).
