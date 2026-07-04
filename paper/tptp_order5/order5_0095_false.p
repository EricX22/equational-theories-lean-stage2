% order5_0095  eq1=47619 eq2=28901  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,W,X,Y,Z] : ( f(X,Y) = f(f(Z,W),f(f(W,Z),U)) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(f(f(Y,Z),X),Y),f(Y,Y)) )).
