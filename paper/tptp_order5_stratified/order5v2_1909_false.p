% order5v2_1909  eq1=52692 eq2=49932  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( f(X,Y) = f(f(f(Z,f(Y,W)),Y),Y) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,Y) != f(f(Z,f(X,f(X,Y))),Y) )).
