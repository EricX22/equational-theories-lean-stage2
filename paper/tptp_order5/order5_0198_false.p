% order5_0198  eq1=3780 eq2=48556  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( f(X,Y) = f(f(Y,Z),f(W,X)) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,X) != f(f(f(X,X),Y),f(Z,X)) )).
