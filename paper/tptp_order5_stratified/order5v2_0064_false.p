% order5v2_0064  eq1=39616 eq2=4658  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(f(f(Y,Z),f(Z,W)),Y),W) )).
fof(neg, negated_conjecture, ? [X,Y] : ( f(f(X,Y),Y) != f(f(Y,X),X) )).
