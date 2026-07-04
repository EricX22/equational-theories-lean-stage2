% order5_0062  eq1=59990 eq2=38497  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( f(f(X,X),X) = f(f(Y,Z),f(Z,Y)) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(f(f(Y,f(f(Y,Z),Z)),W),Z) )).
