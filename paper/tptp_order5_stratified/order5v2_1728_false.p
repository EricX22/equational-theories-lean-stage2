% order5v2_1728  eq1=49017 eq2=45260  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( f(X,Y) = f(f(f(Y,Z),Z),f(Z,Z)) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,Y) != f(X,f(f(f(X,Z),X),X)) )).
