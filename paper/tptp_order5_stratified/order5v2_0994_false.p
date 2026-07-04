% order5v2_0994  eq1=2138 eq2=24732  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y] : ( X = f(f(f(Y,Y),Y),f(Y,Y)) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(f(f(Y,Z),W),f(f(X,Y),Z)) )).
