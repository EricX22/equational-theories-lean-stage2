% order5v2_0653  eq1=29144 eq2=62055  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(f(f(Y,Z),W),Y),f(Y,W)) )).
fof(neg, negated_conjecture, ? [X,Y] : ( f(f(X,Y),Y) != f(f(f(X,X),X),Y) )).
