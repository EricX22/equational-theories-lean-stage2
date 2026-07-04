% order5v2_0486  eq1=39607 eq2=3536  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,W,X,Y,Z] : ( X = f(f(f(f(Y,Z),f(Z,Z)),W),U) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,Y) != f(X,f(f(Z,Z),X)) )).
