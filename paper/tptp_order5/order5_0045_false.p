% order5_0045  eq1=47077 eq2=51857  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( f(X,Y) = f(f(X,Z),f(f(X,Z),Y)) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,Y) != f(f(f(Z,Z),f(Y,Y)),Y) )).
