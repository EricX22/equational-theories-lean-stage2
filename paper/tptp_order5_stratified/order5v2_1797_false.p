% order5v2_1797  eq1=40942 eq2=47234  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(f(f(f(Y,X),Z),X),W),Y) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(X,Y) != f(f(Y,Z),f(f(X,W),W)) )).
