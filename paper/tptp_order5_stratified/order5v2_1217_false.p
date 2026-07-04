% order5v2_1217  eq1=48931 eq2=53295  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( f(X,Y) = f(f(f(Y,X),Z),f(W,X)) )).
fof(neg, negated_conjecture, ? [X,Y] : ( f(X,Y) != f(f(f(f(Y,X),Y),X),Y) )).
