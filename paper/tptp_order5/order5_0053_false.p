% order5_0053  eq1=60894 eq2=61788  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( f(f(X,X),Y) = f(f(X,f(Y,Z)),W) )).
fof(neg, negated_conjecture, ? [U,W,X,Y,Z] : ( f(f(X,X),Y) != f(f(f(X,Z),W),U) )).
